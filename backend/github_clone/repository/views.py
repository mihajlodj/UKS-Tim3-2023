import base64
import json
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main import gitea_service
from main import permissions
from main.models import Commit, Watches
from main.models import Project, WorksOn, Developer, Branch, AccessModifiers
from repository.serializers import RepositorySerializer, DeveloperSerializer


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
def get_all_repos(request, query):
    owner = ''
    is_public = None
    followers = None
    stars = None
    created_date = None
    language = ''

    parts = query.split('&')
    for part in parts:
        if 'owner:' in part:
            owner = part.split('owner:', 1)[1].strip()
        elif 'is:' in part:
            is_public = True if part.split('is:', 1)[1].strip() == 'public' else False
        elif 'followers:' in part:
            followers = int(part.split('followers:', 1)[1].strip())
        elif 'stars:' in part:
            stars = int(part.split('stars:', 1)[1].strip())
        elif 'created:' in part:
            created_date = datetime.strptime(part.split('created:', 1)[1].strip(), '%d-%m-%Y').date()
        elif 'language:' in part:
            language = part.split('language:', 1)[1].strip()
        else:
            query = part.strip()

    cache_key = f"query_repo:{query}:{owner}:{is_public}:{followers}:{stars}:{created_date}:{language}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    results = WorksOn.objects.filter(role__icontains="Owner")

    if query:
        results = results.filter(project__name__icontains=query)
    if owner:
        results = results.filter(developer__user__username__contains=owner)
    if is_public is not None:
        if is_public:
            results = results.filter(project__access_modifier__contains="Public")
        if not is_public:
            results = results.filter(project__access_modifier__contains="Private")
    if created_date:
        results = results.filter(project__timestamp__gte=created_date)

    if results.exists():
        serialized_data = []
        for result in results:
            isExcluded = False
            project_serializer = RepositorySerializer(result.project)
            project = project_serializer.data

            # TODO programski jezik repoa mozda preko giteee moze !?!?
            # if language:
            #     results = results.filter(language__icontain=language)
            if followers is not None:
                allWatches = len(Watches.objects.filter(project__name=project['name']))
                if allWatches < followers:
                    results = results.exclude(project__name__exact=project['name'])
                    isExcluded = True
            if stars is not None:
                allStars = len(Watches.objects.filter(project__name=project['name']))
                if allStars < stars:
                    results = results.exclude(project__name__exact=project['name'])
                    isExcluded = True

            developer_serializer = DeveloperSerializer(result.developer)
            developer = developer_serializer.data

            if not isExcluded:
                serialized_data.append({'developer': developer, 'project': project})

        cache.set(cache_key, serialized_data, timeout=30)

        return Response(serialized_data, status=status.HTTP_200_OK)
    else:
        return Response([], status=status.HTTP_200_OK)


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
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.CanViewRepository])
def get_root_files(request, owner_username, repository_name, ref):
    cache_key = f"root_files:{owner_username}:{repository_name}:{ref}"
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    result = gitea_service.get_root_content(owner_username, repository_name, ref)
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


def save_commit(request, repository_name, json_data, timestamp, commit_sha):
    author = Developer.objects.get(user__username=request.user.username)
    branch = Branch.objects.get(project__name=repository_name, name=json_data['branch'])
    Commit.objects.create(hash=commit_sha, author=author, committer=author, branch=branch, timestamp=timestamp,
                          message=json_data['message'], additional_description=json_data['additional_text'])
