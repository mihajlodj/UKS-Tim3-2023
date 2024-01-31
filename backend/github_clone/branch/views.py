from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.response import Response
from branch.serializers import BranchSerializer
from main.models import Project, WorksOn, Branch, Commit, PullRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from main import gitea_service
import threading


class CreateBranchView(generics.CreateAPIView):
    queryset = Branch.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BranchSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_branches(request, repository_name):
    check_view_permission(request, repository_name)
    result = []
    branches = Branch.objects.filter(project__name=repository_name)
    for branch in branches:
        obj = {
            'name': branch.name,
            'created_by': branch.created_by.user.username
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


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_branch(request, repository_name, branch_name):
    try:
        branch = Branch.objects.get(name=branch_name)
        repository = Project.objects.get(name=repository_name)
        check_delete_permission(request, repository)
        threading.Thread(target=gitea_service.delete_branch, args=([request.user.username, repository_name, branch_name]), kwargs={}).start()
        branch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


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
    
    
def check_delete_permission(request, repo):
    logged_user = request.user.username
    owner = WorksOn.objects.get(project__name=repo.name, role='Owner')
    if owner.developer.user.username != logged_user:
        raise PermissionDenied()
    