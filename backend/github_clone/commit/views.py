from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from main import permissions, gitea_service
from main.models import Role, WorksOn
from pull_request import diff_parser


@api_view(['GET'])
@permission_classes([permissions.CanViewRepository])
def get_diff(request, repository_name, sha):
    owner_username = WorksOn.objects.get(role=Role.OWNER, project__name=repository_name).developer.user.username
    gitea_response = gitea_service.get_commit_diff(owner_username, repository_name, sha)
    diff, overall_additions, overall_deletions = diff_parser.parse_diff(gitea_response.text)
    result = {
        'diff': diff,
        'overall_additions': overall_additions,
        'overall_deletions': overall_deletions
    }
    return Response(result, status=status.HTTP_200_OK)

