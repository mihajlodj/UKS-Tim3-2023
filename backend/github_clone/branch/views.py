from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from main.models import Project, WorksOn, Developer, Branch, Commit, PullRequest
from rest_framework.decorators import api_view, permission_classes
from repository.serializers import RepositorySerializer, DeveloperSerializer
from main.gitea_service import get_root_content, get_repository, get_folder_content, delete_repository
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_branches(request, owner_username, repository_name):
    print(owner_username)
    check_view_permission(request, repository_name)
    result = []
    # name, updated-avatar, updated-timestamp, pull-request id, pull-request status
    branches = Branch.objects.filter(project__name=repository_name)
    for branch in branches:
        obj = {
            'name': branch.name
        }
        try:
            latest_commit = Commit.objects.filter(branch=branch).latest('timestamp')
            obj['updated_timestamp'] = latest_commit.timestamp
            obj['updated_username'] = latest_commit.author.user.username
            obj['updated_avatar'] = latest_commit.author.avatar
        except ObjectDoesNotExist:
            print("No commits found for the specified branch.")
        try:
            latest_pr = PullRequest.objects.filter(source=branch).latest('timestamp')
            obj['pr_id'] = latest_pr.id
            obj['pr_status'] = latest_pr.status 
        except ObjectDoesNotExist:
            print("No PRs found for the specified branch.")
        result.append(obj)
    return Response(result, status=status.HTTP_200_OK)


def check_view_permission(request, repo_name):
    logged_user = request.user.username
    try:
        repo = Project.objects.get(name=repo_name)
        if repo.access_modifier == 'Private':
            works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repo.name)]
            if logged_user not in works_on_list:
                raise PermissionDenied()
    except ObjectDoesNotExist:
        raise Http404()
    