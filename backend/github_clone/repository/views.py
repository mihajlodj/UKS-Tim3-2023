import base64
import json
from django.utils import timezone

from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main import gitea_service
from main import permissions
from main.models import Project, Role, WorksOn, Developer, Branch, AccessModifiers, Invitation, Commit
from repository.serializers import RepositorySerializer, DeveloperSerializer
from developer import service as developer_service
from . import service


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
    permission_classes = (IsAuthenticated, permissions.CanEditRepository,)
    serializer_class = RepositorySerializer
    lookup_field = 'name'


@api_view(['GET'])
@permission_classes([permissions.CanViewRepository])
def get_repo_data_for_display(request, owner_username, repository_name):
    repo = Project.objects.get(name=repository_name)
    gitea_repo_data = gitea_service.get_repository(owner_username, repository_name)
    result = {'name': repo.name, 'description': repo.description, 'access_modifier': repo.access_modifier,
              'default_branch': repo.default_branch.name, 'http': gitea_repo_data['clone_url'],
              'ssh': gitea_repo_data['ssh_url'], 'branches': []}
    branches = Branch.objects.filter(project__name=repository_name)
    branches_names = [b.name for b in branches]
    result['branches'] = branches_names

    branch_commits_overview = {}
    for branch in branches:
        branch_commits = Commit.objects.filter(branch=branch)
        if len(branch_commits) > 0:
            latest_commit_obj = branch_commits.order_by('-timestamp').first()
            latest_commit = {
                'author': {
                    'username': latest_commit_obj.author.user.username,
                    'avatar': developer_service.get_dev_avatar(latest_commit_obj.author.user.username)
                },
                'sha': latest_commit_obj.hash,
                'message': latest_commit_obj.message,
                'timestamp': latest_commit_obj.timestamp,

            }
        branch_commits_overview[branch.name] = {
            'latest_commit': latest_commit,
            'num_commits': len(branch_commits)
        }  
    result['commits_overview'] = branch_commits_overview   
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.CanViewRepository])
def get_root_files(request, owner_username, repository_name, ref):
    cache_key = f"root_files:{owner_username}:{repository_name}:{ref}"
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    result = gitea_service.get_root_content(owner_username, repository_name, ref)
    for item in result:
        last_commit_sha = item['last_commit_sha']
        if Commit.objects.filter(hash=last_commit_sha).exists():
            last_commit = Commit.objects.get(hash=last_commit_sha)
            item['last_commit_message'] = last_commit.message
            item['last_commit_timestamp'] = last_commit.timestamp
        else:
            item['last_commit_message'] = ''
            item['last_commit_timestamp'] = None
    print(result)
    if len(result) != 0:
        cache.set(cache_key, result, timeout=30)

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.CanViewRepository])
def get_folder_files(request, owner_username, repository_name, branch, path):
    cache_key = f"folder_files:{owner_username}:{repository_name}:{branch}:{path}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    result = gitea_service.get_folder_content(owner_username, repository_name, branch, path)
    for item in result:
        last_commit_sha = item['last_commit_sha']
        if Commit.objects.filter(hash=last_commit_sha).exists():
            last_commit = Commit.objects.get(hash=last_commit_sha)
            item['last_commit_message'] = last_commit.message
            item['last_commit_timestamp'] = last_commit.timestamp
        else:
            item['last_commit_message'] = ''
            item['last_commit_timestamp'] = None

    print(result)

    if len(result) != 0:
        cache.set(cache_key, result, timeout=30)

    return Response(result, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, permissions.CanDeleteRepository])
def delete_repo(request, owner_username, repository_name):
    if not Project.objects.filter(name=repository_name).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    repository = Project.objects.get(name=repository_name)
    works_on_list = WorksOn.objects.filter(project__name=repository_name)
    for item in works_on_list:
        item.delete()
    gitea_service.delete_repository(owner_username, repository_name)
    repository.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.CanViewRepository])
def get_file(request, owner_username, repository_name, branch, path):
    cache_key = f"file:{owner_username}:{repository_name}:{branch}:{path}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    file_data = gitea_service.get_file(owner_username, repository_name, branch, path)

    content = file_data['content']
    is_text = True
    try:
        content_bytes = file_data.get('content', '').encode('utf-8')
        content = base64.b64decode(content_bytes).decode('utf-8')
    except UnicodeDecodeError:
        is_text = False

    result = {
        'content': content, 'name': file_data['name'], 'path': file_data['path'],
        'last_commit_sha': file_data['last_commit_sha'], 'size': file_data['size'],
        'url': file_data['url'], 'html_url': file_data['html_url'], 'download_url': file_data['download_url'],
        'is_text': is_text
    }

    cache.set(cache_key, result, timeout=30)

    return Response(result, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def delete_file(request, owner_username, repository_name, path):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
        timestamp = timezone.localtime(timezone.now())
        formatted_datetime = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        old_file = gitea_service.get_file(owner_username, repository_name, json_data['branch'], path)

        commit_data = {
            'author': {'email': request.user.email, 'name': f'{request.user.first_name} {request.user.last_name}'},
            'branch': json_data['branch'],
            'committer': {'email': request.user.email, 'name': f'{request.user.first_name} {request.user.last_name}'},
            'dates': {'author': formatted_datetime, 'committer': formatted_datetime},
            'message': json_data['message'],
            'sha': old_file['sha']
        }
        commit_sha = gitea_service.delete_file(owner_username, repository_name, path, commit_data)
        save_commit(request, repository_name, json_data, timestamp, commit_sha)
        return Response(status=status.HTTP_200_OK)
    except Exception as ex:
        print(ex)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def create_file(request, owner_username, repository_name, path):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
        base64_bytes = base64.b64encode(json_data['content'].encode("utf-8"))
        content = base64_bytes.decode("utf-8")
        timestamp = timezone.localtime(timezone.now())
        formatted_datetime = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        commit_data = {
            'author': {'email': request.user.email, 'name': f'{request.user.first_name} {request.user.last_name}'},
            'branch': json_data['branch'],
            'committer': {'email': request.user.email, 'name': f'{request.user.first_name} {request.user.last_name}'},
            'content': content,
            'dates': {'author': formatted_datetime, 'committer': formatted_datetime},
            'message': json_data['message'],
        }
        commit_sha = gitea_service.create_file(owner_username, repository_name, path, commit_data)
        save_commit(request, repository_name, json_data, timestamp, commit_sha)
        return Response(status=status.HTTP_200_OK)
    except Exception as ex:
        print(ex)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def edit_file(request, owner_username, repository_name, path):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
        base64_bytes = base64.b64encode(json_data['content'].encode("utf-8"))
        content = base64_bytes.decode("utf-8")

        timestamp = timezone.localtime(timezone.now())
        formatted_datetime = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        old_file = gitea_service.get_file(owner_username, repository_name, json_data['branch'], json_data['from_path'])
        commit_data = {
            'author': {'email': request.user.email, 'name': f'{request.user.first_name} {request.user.last_name}'},
            'branch': json_data['branch'],
            'committer': {'email': request.user.email, 'name': f'{request.user.first_name} {request.user.last_name}'},
            'content': content,
            'dates': {'author': formatted_datetime, 'committer': formatted_datetime},
            'from_path': json_data['from_path'],
            'message': json_data['message'],
            'sha': old_file['sha']
        }
        commit_sha = gitea_service.edit_file(owner_username, repository_name, path, commit_data)
        save_commit(request, repository_name, json_data, timestamp, commit_sha)
        return Response(status=status.HTTP_200_OK)
    except Exception as ex:
        print(ex)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def upload_files(request, owner_username, repository_name):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
        files = [{'path': f['name'], 'operation': 'create', 'content': f['content']} for f in json_data['files']]
        timestamp = timezone.localtime(timezone.now())
        formatted_datetime = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        commit_data = {
            'author': {'email': request.user.email, 'name': f'{request.user.first_name} {request.user.last_name}'},
            'branch': json_data['branch'],
            'committer': {'email': request.user.email, 'name': f'{request.user.first_name} {request.user.last_name}'},
            'files': files,
            'dates': {'author': formatted_datetime, 'committer': formatted_datetime},
            'message': json_data['message'],
        }
        commit_sha = gitea_service.upload_files(owner_username, repository_name, commit_data)
        save_commit(request, repository_name, json_data, timestamp, commit_sha)
        return Response(status=status.HTTP_200_OK)
    except Exception as ex:
        print(ex)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users_repo(request, owner_username):
    user = User.objects.get(username=owner_username)
    developer = Developer.objects.get(user_id=user.id)

    cache_key = f"repos:{developer.id}"
    cached_data = cache.get(cache_key)
    if cached_data is not None and (len(cached_data) != 0 or str(cached_data) == "None"):
        return Response(cached_data, status=status.HTTP_200_OK)

    repos = []
    for temp_repo in WorksOn.objects.filter(developer_id=developer.id):
        repo = Project.objects.get(id=temp_repo.project_id)
        is_private = repo.access_modifier == AccessModifiers.PRIVATE
        result = {'name': repo.name, 'description': repo.description, 'access_modifier': is_private,
                  'default_branch': repo.default_branch.name}
        repos.append(result)
    cache.set(cache_key, repos, timeout=30)
    return Response(repos, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, permissions.CanInviteCollaborator])
def invite_collaborator(request, repository_name, invited_username):
    developer = Developer.objects.filter(user__username=invited_username)
    project = Project.objects.filter(name=repository_name)
    if developer.exists() and project.exists:
        developer = developer.first()
        project = project.first()
        if WorksOn.objects.filter(developer=developer, project=project):
            return Response("User already works on repository", status=status.HTTP_400_BAD_REQUEST)
        if Invitation.objects.filter(developer=developer, project=project):
            return Response("User already invited to repository", status=status.HTTP_400_BAD_REQUEST)
        
        Invitation.objects.create(developer=developer, project=project)
        service.invite_collaborator(developer, request.user.username, project)
        
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_invitation(request, repository_name, invited_username, choice):
    developer = Developer.objects.filter(user__username=invited_username)
    project = Project.objects.filter(name=repository_name)
    invitation = Invitation.objects.filter(developer__user__username=invited_username, project__name=repository_name)
    if developer.exists() and project.exists and invitation.exists():
        developer = developer.first()
        project = project.first()
        invitation = invitation.first()

        Invitation.objects.filter(developer__user__username=invited_username, project__name=repository_name).delete()

        if (choice == 'accept'):
            WorksOn.objects.create(developer=developer, project=project, role=Role.DEVELOPER)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invitation(request, repository_name, invited_username):
    if request.user.username != invited_username:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    project = Project.objects.filter(name=repository_name)
    invitation = Invitation.objects.filter(developer__user__username=invited_username, project__name=repository_name)
    invited_user = Developer.objects.filter(user__username=invited_username)
    if invitation.exists() and project.exists and invited_user.exists():
        invitation = invitation.first()
        project = project.first()
        owner = WorksOn.objects.filter(project=project, role=Role.OWNER).first().developer
        result = {
            'owner_username': owner.user.username, 
            'owner_avatar': developer_service.get_dev_avatar(owner.user.username),
            'invited_user_avatar': developer_service.get_dev_avatar(invited_username)
        }
        return Response(result, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


def save_commit(request, repository_name, json_data, timestamp, commit_sha):
    author = Developer.objects.get(user__username=request.user.username)
    branch = Branch.objects.get(project__name=repository_name, name=json_data['branch'])
    Commit.objects.create(hash=commit_sha, author=author, committer=author, branch=branch, timestamp=timestamp,
                          message=json_data['message'], additional_description=json_data['additional_text'])
    
