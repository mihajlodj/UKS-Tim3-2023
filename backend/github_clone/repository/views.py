import base64
import json
import threading
from django.utils import timezone

from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from main import gitea_service
from main import permissions
from main.models import Developer, Branch, Fork, Invitation, Commit, Watches, Stars, WatchOption, EventHistory, \
    EventTypes
from main.models import Project, WorksOn, Developer, Branch, AccessModifiers, Role
from repository.serializers import RepositorySerializer, DeveloperSerializer
from developer import service as developer_service
from datetime import datetime
from . import service
import re
from websocket import notification_service


class CreateRepositoryView(generics.CreateAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RepositorySerializer


class ReadOwnerView(generics.RetrieveAPIView):
    queryset = Developer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = DeveloperSerializer

    def get_object(self):
        owner_username = self.kwargs.get('username')
        return Developer.objects.get(user__username=owner_username)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository])
def update_repo(request, owner_username, repository_name):
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                      role=Role.OWNER).filter()
    if not works_on.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    project = works_on.first().project
    json_data = json.loads(request.body.decode('utf-8'))
    new_name = json_data.get('name', project.name)
    if new_name != repository_name:
        if WorksOn.objects.filter(developer__user__username=owner_username, project__name=new_name).exists():
            return Response("Repository with that name already exists", status=status.HTTP_400_BAD_REQUEST)
    new_description = json_data.get('description', project.description)
    new_access_modifier = json_data.get('access_modifier', project.access_modifier)
    new_default_branch_name = json_data.get('default_branch_name', project.default_branch.name)
    pattern = re.compile(r'^[a-zA-Z][\w-]*$')
    if not pattern.match(new_name) or not pattern.match(new_default_branch_name) or (
            new_access_modifier != AccessModifiers.PRIVATE and new_access_modifier != AccessModifiers.PUBLIC):
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
    project.name = new_name
    project.description = new_description
    project.access_modifier = new_access_modifier

    if new_default_branch_name != project.default_branch.name:
        if Branch.objects.filter(name=new_default_branch_name, project=project).exists():
            branch = Branch.objects.get(name=new_default_branch_name, project=project)
            project.default_branch = branch
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    project.save()
    threading.Thread(target=gitea_service.update_repository, args=([owner_username, project, repository_name]),
                     kwargs={}).start()
    return Response(
        {'name': project.name, 'description': project.description, 'access_modifier': project.access_modifier},
        status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unstarr_it(request, username, repository_name,owner_username):
    try:
        worksOn = WorksOn.objects.get(project__name=repository_name, role__exact=Role.OWNER,developer__user__username__exact=owner_username)
        star = Stars.objects.get(project=worksOn.project, developer__user__username__exact=username)
        star.delete()
        # TODO verovatno moze bolje nego samo da se ocisti cela kes memorija
        cache.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def starr_it(request, username, repository_name,owner_username):
    try:
        worksOn = WorksOn.objects.get(project__name=repository_name,role__exact=Role.OWNER,developer__user__username__exact=owner_username)
        project = worksOn.project
        developer = Developer.objects.get(user__username__exact=username)
        star = Stars.objects.create(project=project, developer=developer)
        star.save()
        # TODO verovatno moze bolje nego samo da se ocisti cela kes memorija
        cache.clear()
        threading.Thread(target=notification_service.send_notification_repository_starred, args=([owner_username, project, request.user.username]), kwargs={}).start()
        return Response(status=status.HTTP_200_OK)
    except Exception as ex:
        print(ex)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_repos(request, query, username):
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

            developer_serializer = DeveloperSerializer(result.developer)
            developer = developer_serializer.data

            if language != '':
                gitea_project = gitea_service.get_repo_language(developer['user']['username'], project['name'])
                if language != gitea_project['data'][0]['language']:
                    isExcluded = True
                    results = results.exclude(project__name=project['name'])
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

            starred = True
            try:
                starred_instance = Stars.objects.get(developer__user__username__exact=username,
                                                     project__name__exact=project['name'])
            except:
                starred = False

            if not isExcluded:
                serialized_data.append({'developer': developer, 'project': project, 'starred': starred,
                                        'developer_avatar': developer_service.get_dev_avatar(developer['user']['username'])})

        cache.set(cache_key, serialized_data, timeout=30)

        return Response(serialized_data, status=status.HTTP_200_OK)
    else:
        return Response([], status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_users_repo(request, owner_username):
    user = User.objects.get(username=owner_username)
    developer = Developer.objects.get(user_id=user.id)

    cache_key = f"repos:{developer.id}"
    cached_data = cache.get(cache_key)
    if cached_data is not None and (len(cached_data) != 0 or str(cached_data) == "None"):
        return Response(cached_data, status=status.HTTP_200_OK)

    repos = []
    for temp_repo in WorksOn.objects.filter(developer_id=developer.id,role=Role.OWNER):
        repo = Project.objects.get(id=temp_repo.project_id)
        is_private = repo.access_modifier == AccessModifiers.PRIVATE
        result = {'name': repo.name, 'description': repo.description, 'access_modifier': is_private,
                  'default_branch': repo.default_branch.name}
        repos.append(result)
    cache.set(cache_key, repos, timeout=30)
    return Response(repos, status=status.HTTP_200_OK)





@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_users_working_on_repos(request, username):
    user = User.objects.get(username=username)
    developer = Developer.objects.get(user_id=user.id)

    cache_key = f"repos:{developer.id}"
    cached_data = cache.get(cache_key)
    if cached_data is not None and (len(cached_data) != 0 or str(cached_data) == "None"):
        return Response(cached_data, status=status.HTTP_200_OK)

    repos = []
    for temp_repo in WorksOn.objects.filter(developer_id=developer.id):
        repo = Project.objects.get(id=temp_repo.project_id)
        is_private = repo.access_modifier == AccessModifiers.PRIVATE
        temp_repos_owner = WorksOn.objects.get(project=repo,role=Role.OWNER)

        print("TEMP REPO OWNER",temp_repos_owner.developer.user.username)

        result = {'name': repo.name, 'description': repo.description, 'access_modifier': is_private,
                  'default_branch': repo.default_branch.name, 'repos_owner': temp_repos_owner.developer.user.username,
                  'repos_owner_avatar': developer_service.get_dev_avatar(temp_repos_owner.developer.user.username)}
        repos.append(result)
    cache.set(cache_key, repos, timeout=30)
    return Response(repos, status=status.HTTP_200_OK)










@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_starred_user_repos(request, username):
    starred_repos = []
    for temp_repo in Stars.objects.filter(developer__user__username__exact=username):
        repo = Project.objects.get(id=temp_repo.project_id)
        is_private = repo.access_modifier == AccessModifiers.PRIVATE
        result = {'name': repo.name, 'description': repo.description, 'access_modifier': is_private,
                  'default_branch': repo.default_branch.name}
        starred_repos.append(result)
    return Response(starred_repos, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_repo_data_for_display(request, owner_username, repository_name, logged_user):
    star = True
    try:
        starred_instance = Stars.objects.get(developer__user__username__exact=logged_user,
                                             project__name__exact=repository_name)
    except:
        star = False

    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                      role=Role.OWNER)
    if not works_on.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    repo = works_on.first().project

    gitea_repo_data = gitea_service.get_repository(owner_username, repository_name)
    result = {'name': repo.name, 'description': repo.description, 'access_modifier': repo.access_modifier,
              'default_branch': repo.default_branch.name, 'http': gitea_repo_data['clone_url'],
              'ssh': gitea_repo_data['ssh_url'], 'branches': [], 'star': star, 'watch': get_watch_info(request, repo)}
    branches = Branch.objects.filter(project=repo)
    branches_names = [b.name for b in branches]
    result['branches'] = branches_names
    result['commits_overview'] = get_branch_commits_overview(branches)

    if Fork.objects.filter(developer__user__username=owner_username, destination__name=repository_name).exists():
        source_repo = Fork.objects.filter(developer__user__username=owner_username,
                                          destination__name=repository_name).first().source
        source_repo_owner = WorksOn.objects.get(project=source_repo, role=Role.OWNER).developer.user.username
        result['forked_from'] = {
            'repository_name': source_repo.name,
            'owner_username': source_repo_owner
        }
    return Response(result, status=status.HTTP_200_OK)


def get_branch_commits_overview(branches):
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
    for branch in branches:
        if branch.name not in branch_commits_overview and branch.parent is not None and branch.parent.name in branch_commits_overview:
            branch_commits_overview[branch.name] = branch_commits_overview[branch.parent.name]
    return branch_commits_overview

def get_watch_info(request, repo):
    watch_option = WatchOption.PARTICIPATING
    issue_events = pull_events = release_events = False
    if Watches.objects.filter(developer__user__username=request.user.username, project=repo).exists():
        obj = Watches.objects.get(developer__user__username=request.user.username, project=repo)
        watch_option = obj.option
        issue_events = obj.issue_events
        pull_events = obj.pull_events
        release_events = obj.release_events
    return {'option': watch_option, 'issue_events': issue_events, 'pull_events': pull_events, 'release_events': release_events}


@api_view(['GET'])
@permission_classes([AllowAny])
def is_users_repo(request, owner_username, repository_name):
    worksOn = WorksOn.objects.get(developer__user__username__exact=owner_username, role__exact=Role.OWNER,
                                  project__name=repository_name)
    result = False
    if worksOn:
        result = True
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.CanViewRepository])
def get_root_files(request, owner_username, repository_name, ref):
    cache_key = f"root_files:{owner_username}:{repository_name}:{ref}"
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    result = gitea_service.get_root_content(owner_username, repository_name, ref)

    works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name,
                                   role=Role.OWNER)
    repository = works_on.project

    for item in result:
        last_commit_sha = item['last_commit_sha']
        if Commit.objects.filter(branch__project=repository, branch__name=ref, hash=last_commit_sha).exists():
            last_commit = Commit.objects.get(branch__project=repository, branch__name=ref, hash=last_commit_sha)
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

    works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name,
                                   role=Role.OWNER)
    repository = works_on.project

    result = gitea_service.get_folder_content(owner_username, repository_name, branch, path)
    for item in result:
        last_commit_sha = item['last_commit_sha']
        if Commit.objects.filter(branch__project=repository, branch__name=branch, hash=last_commit_sha).exists():
            last_commit = Commit.objects.get(branch__project=repository, branch__name=branch, hash=last_commit_sha)
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
    project = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name,
                                  role=Role.OWNER).project
    works_on_list = WorksOn.objects.filter(project=project)
    for item in works_on_list:
        item.delete()
    gitea_service.delete_repository(owner_username, repository_name)
    project.delete()
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
        save_commit(request, owner_username, repository_name, json_data, timestamp, commit_sha)
        send_notification_default_branch_push(owner_username, repository_name, json_data, request)
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
        save_commit(request, owner_username, repository_name, json_data, timestamp, commit_sha)
        send_notification_default_branch_push(owner_username, repository_name, json_data, request)
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
        save_commit(request, owner_username, repository_name, json_data, timestamp, commit_sha)
        send_notification_default_branch_push(owner_username, repository_name, json_data, request)
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
        save_commit(request, owner_username, repository_name, json_data, timestamp, commit_sha)
        send_notification_default_branch_push(owner_username, repository_name, json_data, request)
        return Response(status=status.HTTP_200_OK)
    except Exception as ex:
        print(ex)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

def send_notification_default_branch_push(owner_username, repository_name, json_data, request):
    repository = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).project
    if repository.default_branch.name == json_data['branch']:
        threading.Thread(target=notification_service.send_notification_default_branch_push, \
                            args=([owner_username, repository, {'author': request.user.username, 'message': json_data['message']}]), kwargs={}).start()


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_all_users_repo(request, owner_username):
#     user = User.objects.get(username=owner_username)
#     developer = Developer.objects.get(user_id=user.id)
#
#     cache_key = f"repos:{developer.id}"
#     cached_data = cache.get(cache_key)
#     if cached_data is not None and (len(cached_data) != 0 or str(cached_data) == "None"):
#         return Response(cached_data, status=status.HTTP_200_OK)
#
#     repos = []
#     for temp_repo in WorksOn.objects.filter(developer_id=developer.id):
#         repo = Project.objects.get(id=temp_repo.project_id)
#         is_private = repo.access_modifier == AccessModifiers.PRIVATE
#         result = {'name': repo.name, 'description': repo.description, 'access_modifier': is_private,
#                   'default_branch': repo.default_branch.name}
#         repos.append(result)
#     cache.set(cache_key, repos, timeout=30)
#     return Response(repos, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, permissions.CanInviteCollaborator])
def invite_collaborator(request, owner_username, repository_name, invited_username):
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                      role=Role.OWNER)
    developer = Developer.objects.filter(user__username=invited_username)
    if developer.exists() and works_on.exists():
        developer = developer.first()
        project = works_on.first().project
        if WorksOn.objects.filter(developer=developer, project=project):
            return Response("User already works on repository", status=status.HTTP_400_BAD_REQUEST)
        if Invitation.objects.filter(developer=developer, project=project):
            return Response("User already invited to repository", status=status.HTTP_400_BAD_REQUEST)

        json_data = json.loads(request.body.decode('utf-8'))
        service.invite_collaborator(developer, request.user.username, project, json_data['role'])

        collaborator = {
            'username': developer.user.username,
            'avatar': developer_service.get_dev_avatar(developer.user.username),
            'role': 'Pending'
        }
        return Response(collaborator, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_invitation(request, owner_username, repository_name, invited_username, choice):
    developer = Developer.objects.filter(user__username=invited_username)
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                      role=Role.OWNER)
    if developer.exists() and works_on.exists():
        developer = developer.first()
        project = works_on.first().project
        invitation = Invitation.objects.filter(developer__user__username=invited_username, project=project)
        if not invitation.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        invitation = invitation.first()

        if (choice == 'accept'):
            WorksOn.objects.create(developer=developer, project=project, role=invitation.role)
            Watches.objects.create(developer=developer, project=project, option=WatchOption.PARTICIPATING)
            gitea_permissions = 'write'
            if (invitation.role == 'READONLY'):
                gitea_permissions = 'read'
            threading.Thread(target=gitea_service.add_collaborator,
                             args=([owner_username, repository_name, invited_username, gitea_permissions]), kwargs={}).start()

        Invitation.objects.filter(developer__user__username=invited_username, project=project).delete()

        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invitation(request, owner_username, repository_name, invited_username):
    if request.user.username != invited_username:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                      role=Role.OWNER)
    if not works_on.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    project = works_on.first().project
    invitation = Invitation.objects.filter(developer__user__username=invited_username, project=project)
    invited_user = Developer.objects.filter(user__username=invited_username)
    if invitation.exists() and invited_user.exists():
        invitation = invitation.first()
        owner = works_on.first().developer
        result = {
            'owner_username': owner.user.username,
            'owner_avatar': developer_service.get_dev_avatar(owner.user.username),
            'invited_user_avatar': developer_service.get_dev_avatar(invited_username)
        }
        return Response(result, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def get_collaborators_and_pending_invitations(request, owner_username, repository_name):
    project = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name,
                                  role=Role.OWNER).project
    works_on_list = WorksOn.objects.filter(project=project)
    result = [{
        'username': elem.developer.user.username,
        'avatar': developer_service.get_dev_avatar(elem.developer.user.username),
        'role': elem.role,
        'email': elem.developer.user.email,
        'isBanned': elem.developer.banned
    } for elem in works_on_list if elem.developer.user.username != owner_username]

    pending_invitations = Invitation.objects.filter(project=project)
    for invitation in pending_invitations:
        result.append({
            'username': invitation.developer.user.username,
            'avatar': developer_service.get_dev_avatar(invitation.developer.user.username),
            'role': 'Pending',
            'email': invitation.developer.user.email,
            'isBanned': invitation.developer.banned
        })
    return Response(result, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, permissions.CanInviteCollaborator])
def remove_collaborator(request, owner_username, repository_name, collaborator_username):
    project = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name,
                                  role=Role.OWNER).project
    if WorksOn.objects.filter(project=project, developer__user__username=collaborator_username).exists():
        worksOn = WorksOn.objects.filter(project=project, developer__user__username=collaborator_username).first()
        if worksOn.role != Role.OWNER and collaborator_username != request.user.username:
            worksOn.delete()
            threading.Thread(target=gitea_service.delete_collaborator,
                             args=([owner_username, repository_name, collaborator_username]), kwargs={}).start()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if Invitation.objects.filter(project=project, developer__user__username=collaborator_username).exists():
        invitation = Invitation.objects.filter(project=project, developer__user__username=collaborator_username).first()
        invitation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanInviteCollaborator])
def change_role(request, owner_username, repository_name, collaborator_username):
    developer = Developer.objects.filter(user__username=collaborator_username)
    project = Project.objects.filter(name=repository_name)
    if developer.exists() and project.exists():
        developer = developer.first()
        project = project.first()
        if not WorksOn.objects.filter(developer=developer, project=project):
            return Response("User not a collaborator", status=status.HTTP_400_BAD_REQUEST)
        works_on = WorksOn.objects.filter(developer=developer, project=project).first()

        new_role = json.loads(request.body.decode('utf-8'))['role']
        if new_role != Role.READONLY and new_role != Role.DEVELOPER and new_role != Role.MAINTAINER:
            return Response("Invalid role", status=status.HTTP_400_BAD_REQUEST)

        if new_role != works_on.role:
            works_on.role = new_role
            works_on.save()

            gitea_permissions = 'write'
            if (new_role == Role.READONLY):
                gitea_permissions = 'read'
            threading.Thread(target=gitea_service.change_collaborator_role,
                             args=([owner_username, repository_name, collaborator_username, gitea_permissions]),
                             kwargs={}).start()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated, permissions.CanTransferOwnership])
def transfer_ownership(request, owner_username, repository_name):
    new_owner_username = json.loads(request.body.decode('utf-8'))['new_owner']
    works_on_old_owner = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                                role=Role.OWNER)
    works_on_new_owner = WorksOn.objects.filter(developer__user__username=new_owner_username,
                                                project__name=repository_name)
    if (not works_on_old_owner.exists() or not works_on_new_owner.exists()):
        return Response(status=status.HTTP_404_NOT_FOUND)
    project = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name,
                                  role=Role.OWNER).project
    old_owner = WorksOn.objects.get(developer__user__username=owner_username, project=project, role=Role.OWNER)
    new_owner = WorksOn.objects.get(developer__user__username=new_owner_username, project=project)
    old_owner.role = Role.MAINTAINER
    new_owner.role = Role.OWNER
    old_owner.save()
    new_owner.save()
    threading.Thread(target=gitea_service.transfer_ownership,
                     args=([owner_username, repository_name, new_owner_username]), kwargs={}).start()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def fork(request, owner_username, repository_name):
    if owner_username == request.user.username:
        return Response("Cannot fork own repository", status=status.HTTP_400_BAD_REQUEST)
    if not WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                  role=Role.OWNER).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name,
                                   role=Role.OWNER)
    new_repo_info = json.loads(request.body.decode('utf-8'))

    new_owner = Developer.objects.get(user__username=request.user.username)
    repository = works_on.project

    service.fork(repository, new_repo_info, owner_username, new_owner)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def save_watch_preferences(request, owner_username, repository_name):
    developer = Developer.objects.get(user__username=request.user.username)
    works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER)
    repository = works_on.project
    payload = json.loads(request.body.decode('utf-8'))
    if not Watches.objects.filter(developer=developer, project=repository).exists():
        Watches.objects.create(
            developer=developer, 
            project=repository, 
            option=payload['option'], 
            issue_events=payload['issue_events'],
            pull_events=payload['pull_events'],
            release_events=payload['release_events']
        )
    else:
        watch_preferences = Watches.objects.get(developer=developer, project=repository)
        watch_preferences.option = payload['option']
        watch_preferences.issue_events = payload['issue_events']
        watch_preferences.pull_events = payload['pull_events']
        watch_preferences.release_events = payload['release_events']
        watch_preferences.save()
    return Response(status=status.HTTP_201_CREATED)


def save_commit(request, owner_username, repository_name, json_data, timestamp, commit_sha):
    project = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name,
                                  role=Role.OWNER).project
    author = Developer.objects.get(user__username=request.user.username)
    branch = Branch.objects.get(project=project, name=json_data['branch'])
    Commit.objects.create(hash=commit_sha, author=author, committer=author, branch=branch, timestamp=timestamp,
                          message=json_data['message'], additional_description=json_data['additional_text'])


@api_view(['GET'])
@permission_classes([AllowAny])
def get_event_history(request, owner_username,repository_name,related_id,event_type):
    worksOn = WorksOn.objects.get(project__name=repository_name,role=Role.OWNER,developer__user__username=owner_username)
    type = ""
    if event_type =="issue":
        type = EventTypes.ISSUE
    elif event_type == "pr":
        type = EventTypes.PULL_REQUEST
    elif event_type == "milestone":
        type = EventTypes.MILESTONE
    events = EventHistory.objects.filter(project=worksOn.project,related_id=related_id,type=type)
    ret_val = []
    for temp_event in events:
        event ={'time':temp_event.time,
                'text':temp_event.text}
        ret_val.append(event)
    return Response(ret_val, status=status.HTTP_200_OK)
