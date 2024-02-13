from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

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
from main import permissions
from main.models import Developer, Issue, Project, Milestone, WorksOn

gitea_base_url = settings.GITEA_BASE_URL
access_token = settings.GITEA_ACCESS_TOKEN


class IssueView(generics.CreateAPIView):
    queryset = Issue.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = IssueSerializer


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_issue(request):
    pk = request.data.get('id')
    reponame = request.data['repoName']
    issue = Issue.objects.get(id=pk)
    issue.title = request.data['title']
    try:
        issue.milestone = Milestone.objects.get(project__name=reponame, title=request.data['milestone'])
    except main.models.Milestone.DoesNotExist:
        pass
    issue.description = request.data['description']
    issue.save()

    # update in gitea
    owner = WorksOn.objects.get(role='Owner', project=issue.project).developer.user.username
    gitea_service.update_issue(owner=owner, repo=reponame, issue=issue, index=issue.id)

    return Response(serialize_issue(issue), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_issue(request, pk):
    try:
        issue = Issue.objects.get(pk=pk)
        return JsonResponse(issue)
    except Exception:
        return JsonResponse([], safe=False, status=200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_issue(request, repo_name, pk):
    issue = Issue.objects.get(pk=pk)
    issue.delete()
    owner = WorksOn.objects.get(role='Owner', project=issue.project).developer.user.username
    gitea_service.delete_issue(owner=owner, repo=repo_name, index=pk)
    return HttpResponse(status=200)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def close_issue(request, repo_name, pk):
    issue = Issue.objects.get(pk=pk)
    issue.open = False
    issue.save()
    owner = WorksOn.objects.get(role='Owner', project=issue.project).developer.user.username
    gitea_service.close_issue(owner=owner, repo=repo_name, issue=issue, index=pk)
    return HttpResponse(status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_issues(request, repo_name):
    projectName = repo_name
    data = []
    for issue in Issue.objects.filter(project__name=projectName).values():
        data.append({
            'id': issue['id'],
            'title': issue['title'],
            'description': issue['description'],
            'open': issue['open'],
            'created': issue['created'],
            'manager': Developer.objects.get(user__id=issue['manager_id']).user.username,
            'project': Project.objects.get(id=issue['project_id']).name,
            'milestone': None if issue['milestone_id'] is None else serialize_milestone(Milestone.objects.get(id=issue['milestone_id']))
        })
    return JsonResponse(data, safe=False, status=200)

def serialize_milestone(milestones):
    return {
        'title': milestones.title,
        'description': milestones.description,
        'state': milestones.state,
        'due_date': milestones.deadline,
    }