from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime
import main
from main import gitea_service
from issue.serializers import IssueSerializer, serialize_issue
from repository.serializers import RepositorySerializer, DeveloperSerializer
from milestone.serializers import MilestoneSerializer
from main import permissions
from main.models import Developer, Issue, Project, Milestone, Role, WorksOn
from django.core.cache import cache

from websocket import notification_service

gitea_base_url = settings.GITEA_BASE_URL
access_token = settings.GITEA_ACCESS_TOKEN


class IssueView(generics.CreateAPIView):
    queryset = Issue.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = IssueSerializer


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def assign_manager(request, owner_username, repo_name):
    dev_username = request.data.get('manager')
    issue_id = int(request.data.get('issue_id'))
    issue = Issue.objects.get(id=issue_id)

    dev = Developer.objects.get(user__username=dev_username)
    issue.manager.add(dev)
    gitea_service.subscribe_user_to_issue(owner_username, repo_name, issue.id, dev_username)
    issue.save()
    return Response(status=200)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def unassign_manager(request, owner_username, repo_name):
    dev_username = request.data.get('manager')
    issue_id = int(request.data.get('issue_id'))
    try:
        issue = Issue.objects.get(id=issue_id)
        dev = Developer.objects.get(user__username=dev_username)
        try:
            issue.manager.remove(dev)
            gitea_service.unsubscribe_user_to_issue(owner_username, repo_name, issue.id, dev_username)
            issue.save()
        except Exception:
            return JsonResponse({'message': 'Assignee removal failed'}, safe=False, status=405)
    except Exception:
        return JsonResponse({'message': 'Developer or issue does not exist'}, safe=False, status=405)
    return Response(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_possible_assignees(request, owner_username, repo_name, issue_id):
    try:
        issue = Issue.objects.get(id=issue_id)
        try:
            managers = [dev.user.username for dev in issue.manager.all()]
            project = issue.project
            worksOnList = WorksOn.objects.filter(project=project, role=Role.DEVELOPER)
            project_devs = [worksOn.developer.user.username for worksOn in worksOnList]
            possible_assignees = [dev for dev in project_devs if dev not in managers]
            return JsonResponse(data=possible_assignees, safe=False, status=200)
        except Exception:
            return JsonResponse({'message': 'Getting possible assignees failed'}, safe=False, status=405)
    except Exception:
        return JsonResponse({'message': 'No issue with this ID'}, safe=False, status=405)


@api_view(['GET'])
def get_all_users_issues(request, logged_user):
    results = Issue.objects.filter(manager__user__username=logged_user)
    if results.exists():
        serialized_data = []
        for result in results:
            serialized_data.append({
            'id': result.id,
            'title': result.title,
            'description': result.description,
            'open': result.open,
            'created': result.created,
            'creator': result.creator.user.username,
            'project': result.project.name,
            'milestone': None if result.milestone is None else serialize_milestone(result.milestone),
            'manager': [] if result.manager is None else [dev.user.username for dev in result.manager.all()]
            })
        return Response(serialized_data, status=status.HTTP_200_OK)
    else:
        return Response([], status=status.HTTP_200_OK)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_issue(request):
    pk = request.data.get('id')
    reponame = request.data['project']
    issue = Issue.objects.get(id=pk)
    issue.title = request.data['title']
    try:
        milestoneId = request.data['milestone']
        if milestoneId is None:
            issue.milestone = None
        else:
            issue.milestone = Milestone.objects.get(project__name=reponame, id=milestoneId)
    except main.models.Milestone.DoesNotExist:
        pass
    except TypeError:
        pass
    issue.description = request.data['description']
    issue.save()

    # update in gitea
    owner = WorksOn.objects.get(role='Owner', project=issue.project).developer.user.username
    gitea_service.update_issue(owner=owner, repo=reponame, issue=issue, index=issue.id)
    notification_service.send_notification_issue_updated(issue, request.user.username)
    return JsonResponse({
            'id': issue.id,
            'title': issue.title,
            'description': issue.description,
            'open': issue.open,
            'created': issue.created,
            'creator': issue.creator.user.username,
            'project': issue.project.name,
            'milestone': None if issue.milestone is None else serialize_milestone(issue.milestone),
            'manager': [] if issue.manager is None else [dev.user.username for dev in issue.manager.all()]
        }, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_issues(request, query):
    creator = ''
    is_open = None
    created_date = None
    assignee = ''

    parts = query.split('&')
    for part in parts:
        if 'owner:' in part:
            creator = part.split('owner:', 1)[1].strip()
        elif 'is:' in part:
            is_open = True if part.split('is:', 1)[1].strip() == 'open' else False
        elif 'assignee:' in part:
            assignee = part.split('assignee:', 1)[1].strip()
        elif 'created:' in part:
            created_date = datetime.strptime(part.split('created:', 1)[1].strip(), '%d-%m-%Y').date()
        else:
            query = part.strip()

    # print(creator ,"->creator",is_open,"->is_open",assignee,"->assignee",created_date,"->created_date",query,"->query")

    cache_key = f"issue_query:{query}:{creator}:{is_open}:{assignee}:{created_date}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    results = Issue.objects.all()

    if query:
        results = results.filter(title__contains=query)
    if creator:
        results = results.filter(creator__user__username__contains=creator)
    if assignee:
        results = results.filter(manager__user__username__contains=assignee)
    if is_open is not None:
        if is_open:
            results = results.filter(open=True)
        if not is_open:
            results = results.filter(open=False)
    if created_date:
        results = results.filter(created__gte=created_date)

    if results.exists():
        serialized_data = []
        for result in results:
            project_serializer = RepositorySerializer(result.project)
            project = project_serializer.data

            works_on = WorksOn.objects.get(project=result.project,role=Role.OWNER)

            developer_serializer = DeveloperSerializer(result.creator)
            developer = developer_serializer.data

            milestone_serializer = MilestoneSerializer(result.milestone)
            milestone = milestone_serializer.data

            managers_data = []
            for manager in result.manager.all():
                manager_serializer = DeveloperSerializer(manager)
                managers_data.append(manager_serializer.data)

            serialized_data.append(
                {'created': result.created, 'developer': developer, 'project': project, 'title': result.title,
                 'description': result.description, 'milestone': milestone, 'open': result.open, 'managers':managers_data,
                 'issueid': result.id, 'repo_owner_username': works_on.developer.user.username, 'milestone_id': result.milestone_id})

        cache.set(cache_key, serialized_data, timeout=30)

        return Response(serialized_data, status=status.HTTP_200_OK)
    else:
        return Response([], status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_issue(request, pk):
    try:
        issue = Issue.objects.get(pk=pk)
        creator = Developer.objects.get(id=issue.creator.id)
        serialized_issue = {
            'id': issue.id,
            'title': issue.title,
            'description': issue.description,
            'open': issue.open,
            'created': issue.created,
            'creator': {
                'username': creator.user.username,
                'avatar': creator.avatar
            },
            'labels': [],
            'project': Project.objects.get(id=issue.project.id).name,
            'milestone': None if issue.milestone is None else serialize_milestone(
                Milestone.objects.get(id=issue.milestone.id)),
            'manager': [dev.user.username for dev in issue.manager.all()]
        }

        from_issue_labels = issue.labels.all()
        for label in from_issue_labels:
            serialized_issue['labels'].append({
                'id': label.id,
                'name': label.name,
                'description': label.description
            })

        return JsonResponse(serialized_issue, safe=False, status=200)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_issue(request, repo_name, pk):
    try:
        issue = Issue.objects.get(pk=pk)
        issue.delete()
        owner = WorksOn.objects.get(role='Owner', project=issue.project).developer.user.username
        gitea_service.delete_issue(owner=owner, repo=repo_name, index=pk)

        return HttpResponse(status=200)
    except BaseException:
        return HttpResponse(content="Issue doesn't exist", status=400)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def close_issue(request, repo_name, pk):
    issue = Issue.objects.get(pk=pk)
    issue.open = False
    issue.save()
    owner = WorksOn.objects.get(role='Owner', project=issue.project).developer.user.username
    gitea_service.close_issue(owner=owner, repo=repo_name, issue=issue, index=pk)
    notification_service.send_notification_issue(issue, 'closed', request.user.username)
    return HttpResponse(status=200)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def reopen_issue(request, repo_name, pk):
    issue = Issue.objects.get(pk=pk)
    issue.open = True
    issue.save()
    owner = WorksOn.objects.get(role='Owner', project=issue.project).developer.user.username
    gitea_service.reopen_issue(owner=owner, repo=repo_name, issue=issue, index=pk)
    notification_service.send_notification_issue(issue, 'reopened', request.user.username)
    return HttpResponse(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_issues(request, owner_username, repo_name):
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repo_name, role=Role.OWNER)
    if not works_on.exists():
        return JsonResponse([], safe=False, status=200)
    data = []
    for issue in Issue.objects.filter(project=works_on.first().project):
        data.append({
            'id': issue.id,
            'title': issue.title,
            'description': issue.description,
            'open': issue.open,
            'created': issue.created,
            'creator': issue.creator.user.username,
            'project': issue.project.name,
            'milestone': None if issue.milestone is None else serialize_milestone(issue.milestone),
            'manager': [] if issue.manager is None else [dev.user.username for dev in issue.manager.all()]
        })
    return JsonResponse(data, safe=False, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_issues_linked_with_milestone(request, owner_username, repo_name, milestone_id):
    try:
        works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repo_name)
        issues = Issue.objects.filter(project=works_on.project, milestone_id=milestone_id)
        serialized_issues = serialize_issues(issues)
        return Response(serialized_issues, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        raise Http404()


def serialize_issues(issues):
    serialized_issues = []
    for issue in issues:
        serialized_issue = serialize_issue(issue)
        serialized_issues.append(serialized_issue)
    return serialized_issues


def serialize_issue(issue):
    return {
        'id': issue.id,
        'title': issue.title,
        'description': issue.description,
        'open': issue.open,
        'created': issue.created,
        'creator': Developer.objects.get(id=issue.creator_id).user.username,
        'project': Project.objects.get(id=issue.project_id).name,
        'milestone': None if issue.milestone_id is None else serialize_milestone(
            Milestone.objects.get(id=issue.milestone_id)),
        'tags': []
    }


def serialize_milestone(milestones):
    return {
        'id': milestones.id,
        'title': milestones.title,
        'description': milestones.description,
        'state': milestones.state,
        'due_date': milestones.deadline,
    }
