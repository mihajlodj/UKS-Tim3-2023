from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from main import gitea_service, permissions
import json
from main.models import PullRequest, Branch, Developer, WorksOn, Role, PullRequestStatus
from pull_request import diff_parser, service
from repository.serializers import RepositorySerializer, DeveloperSerializer
from django.core.cache import cache


@api_view(['POST'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def create(request, owner_username, repository_name):
    json_data = json.loads(request.body.decode('utf-8'))
    if PullRequest.objects.filter(project__name=repository_name, source__name=json_data['compare'],
                                  target__name=json_data['base']):
        return Response("Pull request already exists", status=status.HTTP_400_BAD_REQUEST)
    if not Branch.objects.filter(name=json_data['base'], project__name=repository_name).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not Branch.objects.filter(name=json_data['compare'], project__name=repository_name).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    response = gitea_service.create_pull_request(owner_username, repository_name,
                                                 {'base': json_data['base'], 'head': json_data['compare'],
                                                  'title': service.get_pull_title(json_data)})
    if response.status_code == 201:
        id = service.save_pull_request(request.user.username, repository_name, json_data, response)
        return Response({'id': id}, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_pull_reqs(request, query):
    cache_key = f"pull_request_query:{query}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    results = PullRequest.objects.filter(title__contains=query)

    if results.exists():
        serialized_data = []
        for result in results:
            developer_serializer = DeveloperSerializer(result.author)
            author = developer_serializer.data

            project_serializer = RepositorySerializer(result.project)
            project = project_serializer.data

            workson = WorksOn.objects.get(project__name=project['name'], role__exact="Owner")

            serialized_data.append(
                {'title': result.title, 'timestamp': result.timestamp, 'project': project, 'author': author,
                 'Status': result.status, 'developer': workson.developer.user.username})

        cache.set(cache_key, serialized_data, timeout=30)

        return Response(serialized_data, status=status.HTTP_200_OK)
    else:
        return Response([], status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def get_all(request, repository_name):
    requests = PullRequest.objects.filter(project__name=repository_name)
    result = []
    for req in requests:
        obj = {
            'title': req.title, 'status': req.status, 'timestamp': req.timestamp, 'author': req.author.user.username,
            'id': req.gitea_id,
            'labels': [], 'reviews': []
        }
        if req.milestone is not None:
            obj['milestone'] = req.milestone.title
        if req.assignee is not None:
            obj['assignee'] = {'username': req.assignee.user.username,
                               'avatar': service.get_dev_avatar(req.assignee.user.username)}
        result.append(obj)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def get_one(request, repository_name, pull_id):
    # Basic data
    if not PullRequest.objects.filter(project__name=repository_name, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project__name=repository_name, gitea_id=pull_id)
    result = {
        'title': req.title, 'status': req.status, 'timestamp': req.timestamp,
        'author': {'username': req.author.user.username}, 'id': pull_id,
        'labels': [], 'reviews': [], 'reviewers': [], 'mergeable': req.mergeable, 'base': req.target.name,
        'compare': req.source.name,
        'commits': [], 'conflicting_files': [], 'description': req.description
    }
    if req.milestone is not None:
        result['milestone'] = {'id': req.milestone.id, 'title': req.milestone.title}
    if req.assignee is not None:
        result['assignee'] = {'username': req.assignee.user.username,
                              'avatar': service.get_dev_avatar(req.assignee.user.username)}

    # Commits data
    owner_username = WorksOn.objects.get(role=Role.OWNER, project__name=repository_name).developer.user.username
    response = gitea_service.get_pull_request_commits(owner_username, repository_name, pull_id)
    commits_list_json = response.json()
    for commit_data in commits_list_json:
        result['commits'].append({
            'hash': commit_data['sha'],
            'message': commit_data['commit']['message'],
            'timestamp': commit_data['created'],
            'author': service.get_commit_author(commit_data['author']['login'], commit_data['commit']['message'],
                                                repository_name),
            'files': commit_data['files'],
            'stats': commit_data['stats']
        })

    # Diff
    response = gitea_service.get_pull_request_diff(owner_username, repository_name, pull_id)
    diff, overall_additions, overall_deletions = diff_parser.parse_diff(response.text)
    result['diff'] = diff
    result['overall_additions'] = overall_additions
    result['overall_deletions'] = overall_deletions
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def get_possible_assignees(request, repository_name):
    result = []
    works_on_list = WorksOn.objects.filter(project__name=repository_name)
    for obj in works_on_list:
        if obj.role != Role.IS_BANNED:
            result.append({'username': obj.developer.user.username,
                           'avatar': service.get_dev_avatar(obj.developer.user.username)})
    return Response(result, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def update(request, repository_name, pull_id):
    if not PullRequest.objects.filter(project__name=repository_name, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project__name=repository_name, gitea_id=pull_id)
    json_data = json.loads(request.body.decode('utf-8'))
    service.update_milestone(json_data, req)
    service.update_assignee(json_data, req, repository_name)
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def update_title(request, repository_name, pull_id):
    if not PullRequest.objects.filter(project__name=repository_name, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project__name=repository_name, gitea_id=pull_id)
    title = json.loads(request.body.decode('utf-8'))['title']
    if title.strip() != '':
        req.title = title
        req.save()
        return Response(title, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def close(request, repository_name, pull_id):
    if not PullRequest.objects.filter(project__name=repository_name, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project__name=repository_name, gitea_id=pull_id)
    if req.status != PullRequestStatus.OPEN:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    req.status = PullRequestStatus.CLOSED
    req.timestamp = timezone.localtime(timezone.now())
    req.save()
    return Response(req.status, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def reopen(request, repository_name, pull_id):
    if not PullRequest.objects.filter(project__name=repository_name, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project__name=repository_name, gitea_id=pull_id)
    if req.status != PullRequestStatus.CLOSED:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    req.status = PullRequestStatus.OPEN
    req.timestamp = timezone.localtime(timezone.now())
    req.save()
    return Response(req.status, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def mark_as_open(request, repository_name):
    pull_ids = json.loads(request.body.decode('utf-8'))['ids']
    for id in pull_ids:
        if PullRequest.objects.filter(project__name=repository_name, gitea_id=id).exists():
            pull = PullRequest.objects.get(project__name=repository_name, gitea_id=id)
            if pull.status == PullRequestStatus.CLOSED:
                pull.status = PullRequestStatus.OPEN
                pull.timestamp = timezone.localtime(timezone.now())
                pull.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def mark_as_closed(request, repository_name):
    pull_ids = json.loads(request.body.decode('utf-8'))['ids']
    for id in pull_ids:
        if PullRequest.objects.filter(project__name=repository_name, gitea_id=id).exists():
            pull = PullRequest.objects.get(project__name=repository_name, gitea_id=id)
            if pull.status == PullRequestStatus.OPEN:
                pull.status = PullRequestStatus.CLOSED
                pull.timestamp = timezone.localtime(timezone.now())
                pull.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def merge(request, repository_name, pull_id):
    if not PullRequest.objects.filter(project__name=repository_name, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project__name=repository_name, gitea_id=pull_id)
    if req.status != PullRequestStatus.OPEN or not req.mergeable:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    req.status = PullRequestStatus.MERGED
    req.timestamp = timezone.localtime(timezone.now())
    merged_by = Developer.objects.get(user__username=request.user.username)
    req.merged_by = merged_by
    req.save()
    owner_username = WorksOn.objects.get(role=Role.OWNER, project__name=repository_name).developer.user.username
    gitea_service.merge_pull_request(owner_username, repository_name, pull_id)
    return Response(status=status.HTTP_200_OK)
