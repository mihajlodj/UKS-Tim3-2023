from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.response import Response
from branch.serializers import BranchSerializer
from main.gitea_service import get_gitea_user_info_gitea_service
from main.models import Project, WorksOn, Branch, Commit, PullRequest
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from main import gitea_service, permissions
import threading


class CreateBranchView(generics.CreateAPIView):
    queryset = Branch.objects.all()
    permission_classes = (IsAuthenticated,permissions.CanCreateBranch,)
    serializer_class = BranchSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_branches(request, repository_name):
    permissions.can_view_repository(request, Project.objects.get(name=repository_name))
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

            if latest_commit.author.avatar is None:
                gitea_user_info = get_gitea_user_info_gitea_service(latest_commit.author.user.username)
                obj['updated_avatar'] = gitea_user_info['avatar_url']
            else:
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
    permissions.can_edit_repository_content(request, Project.objects.get(name=repository_name))
    try:
        branch = Branch.objects.get(name=branch_name)
        repository = Project.objects.get(name=repository_name)
        threading.Thread(target=gitea_service.delete_branch, args=([request.user.username, repository_name, branch_name]), kwargs={}).start()
        branch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    