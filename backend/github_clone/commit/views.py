from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from main import permissions, gitea_service
from main.models import Role, WorksOn, Commit
from pull_request import diff_parser
from developer import service as dev_service


@api_view(['GET'])
@permission_classes([permissions.CanViewRepository])
def get_diff(request, owner_username, repository_name, sha):
    gitea_response = gitea_service.get_commit_diff(owner_username, repository_name, sha)
    diff, overall_additions, overall_deletions = diff_parser.parse_diff(gitea_response.text)
    result = {
        'diff': diff,
        'overall_additions': overall_additions,
        'overall_deletions': overall_deletions
    }
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.CanViewRepository])
def get(request, owner_username, repository_name, branch, sha):
    project = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).project
    if not Commit.objects.filter(branch__project=project, hash=sha).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    commit = Commit.objects.get(branch__project=project, branch__name=branch, hash=sha)
    result = {
        'sha': sha,
        'message': commit.message,
        'timestamp': commit.timestamp,
        'branch': commit.branch.name,
        'author': {
            'username': commit.author.user.username,
            'avatar': dev_service.get_dev_avatar(commit.author.user.username)
        }
    }
    return Response(result, status=status.HTTP_200_OK)
