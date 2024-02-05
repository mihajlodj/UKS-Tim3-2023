import base64
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from main.models import Commit, Project, WorksOn, Developer, Branch
from rest_framework.decorators import api_view, permission_classes
from repository.serializers import RepositorySerializer, DeveloperSerializer
from main import gitea_service
from rest_framework.exceptions import PermissionDenied
import json
from datetime import datetime


class CreateRepositoryView(generics.CreateAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RepositorySerializer


class ReadOwnerView(generics.RetrieveAPIView):
    queryset = Developer.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = DeveloperSerializer

    def get_object(self):
        owner_username = self.kwargs.get('username')
        return Developer.objects.get(user__username=owner_username)


class UpdateRepositoryView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RepositorySerializer
    lookup_field = 'name'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_repo_data_for_display(request, owner_username, repository_name):
    repo = Project.objects.get(name=repository_name)
    check_view_permission(request, repo)
    gitea_repo_data = gitea_service.get_repository(owner_username, repository_name)
    result = {'name': repo.name, 'description': repo.description, 'access_modifier': repo.access_modifier, 'default_branch': repo.default_branch.name, 
              'http': gitea_repo_data['clone_url'], 'ssh': gitea_repo_data['ssh_url'], 'branches': []}
    branches = Branch.objects.filter(project__name=repository_name)
    branches_names = [b.name for b in branches]
    result['branches'] = branches_names
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_root_files(request, owner_username, repository_name, ref):
    check_view_permission(request, Project.objects.get(name=repository_name))
    return Response(gitea_service.get_root_content(owner_username, repository_name, ref), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_folder_files(request, owner_username, repository_name, branch, path):
    check_view_permission(request, Project.objects.get(name=repository_name))
    return Response(gitea_service.get_folder_content(owner_username, repository_name, branch, path), status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_repo(request, owner_username, repository_name):
    if not Project.objects.filter(name=repository_name).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    repository = Project.objects.get(name=repository_name)
    check_delete_permission(request, repository)
    works_on_list = WorksOn.objects.filter(project__name=repository_name)
    for item in works_on_list:
        item.delete()
    gitea_service.delete_repository(owner_username, repository_name)
    repository.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_file(request, owner_username, repository_name, branch, path):
    check_view_permission(request, Project.objects.get(name=repository_name))
    file_data = gitea_service.get_file(owner_username, repository_name, branch, path)
    content = ''
    try:
        content_bytes = file_data.get('content', '').encode('utf-8')
        content = base64.b64decode(content_bytes).decode('utf-8')
    except UnicodeDecodeError:
        pass
    result = {
        'content': content, 'name': file_data['name'], 'path': file_data['path'], 'last_commit_sha': file_data['last_commit_sha'], 'size': file_data['size'],
        'url': file_data['url'], 'html_url': file_data['html_url'], 'download_url': file_data['download_url']
    }
    return Response(result, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_file(request, owner_username, repository_name, path):
    try:
        raw_data = request.body
        decoded_data = raw_data.decode('utf-8')
        json_data = json.loads(decoded_data)
        
        author_name = f'{request.user.first_name} {request.user.last_name}'
        author_email = request.user.email
        branch_name = json_data['branch']
        content_bytes = json_data['content'].encode("utf-8") 
        base64_bytes = base64.b64encode(content_bytes) 
        content = base64_bytes.decode("utf-8") 
        
        timestamp = datetime.now()
        formatted_datetime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        from_path = json_data['from_path']
        message = json_data['message']
        old_file = gitea_service.get_file(owner_username, repository_name, branch_name, from_path)
        sha = old_file['sha']
        commit_data = {
            'author': {
                'email': author_email,
                'name': author_name
            },
            'branch': branch_name,
            'committer': {
                'email': author_email,
                'name': author_name
            },
            'content': content,
            'dates': {
                'author': formatted_datetime,
                'committer': formatted_datetime
            },
            'from_path': from_path,
            'message': message,
            'sha': sha 
        }
        commit_sha = gitea_service.edit_file(owner_username, repository_name, path, commit_data)

        author = Developer.objects.get(user__username=request.user.username)
        branch = Branch.objects.get(project__name=repository_name, name=branch_name)
        Commit.objects.create(hash=commit_sha, author=author, committer=author, branch=branch, timestamp=timestamp, message=message)

        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)



def check_view_permission(request, repo):
    logged_user = request.user.username
    if repo.access_modifier == 'Private':
        works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repo.name)]
        if logged_user not in works_on_list:
            raise PermissionDenied()


def check_delete_permission(request, repo):
    logged_user = request.user.username
    owner = WorksOn.objects.get(project__name=repo.name, role='Owner')
    if owner.developer.user.username != logged_user:
        raise PermissionDenied()