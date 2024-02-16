from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from main import gitea_service
import json
from main import permissions

@api_view(['POST'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def create(request, owner_username, repository_name):
    json_data = json.loads(request.body.decode('utf-8'))
    response = gitea_service.create_pull_request(owner_username, repository_name, {'base': json_data['base'], 'head': json_data['compare'], 'title': json_data['compare']})
    print(response.status_code)
    print(response.json())
    return Response(status=status.HTTP_200_OK)