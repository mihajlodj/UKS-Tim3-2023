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
from main.models import PullRequest, Branch, Project, Developer

@api_view(['POST'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def create(request, owner_username, repository_name):
    json_data = json.loads(request.body.decode('utf-8'))
    base_name = json_data['base']
    compare_name = json_data['compare']
    title = json_data['title']
    description = json_data['description']
    if not title:
        title = compare_name
    if not Branch.objects.filter(name=base_name, project__name=repository_name).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not Branch.objects.filter(name=compare_name, project__name=repository_name).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    author = Developer.objects.get(user__username=request.user.username)
    response = gitea_service.create_pull_request(owner_username, repository_name, {'base': base_name, 'head': compare_name, 'title': title})
    if response.status_code == 201:
        print(response.json())
        src = Branch.objects.get(name=compare_name, project__name=repository_name)
        dest = Branch.objects.get(name=base_name, project__name=repository_name)
        project = Project.objects.get(name=repository_name)
        PullRequest.objects.create(source=src, target=dest, project=project, author=author, title=title, description=description)
        return Response({'id': response.json()['id']}, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)