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
from main.models import PullRequest, Branch, Project, Developer, Milestone, WorksOn, Role
import re
import git
from unidiff import PatchSet
from io import StringIO

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
        src = Branch.objects.get(name=compare_name, project__name=repository_name)
        dest = Branch.objects.get(name=base_name, project__name=repository_name)
        project = Project.objects.get(name=repository_name)   
        pull = PullRequest.objects.create(source=src, target=dest, project=project, author=author, title=title, description=description)
        if 'milestone_id' in json_data and Milestone.objects.filter(id=json_data['milestone_id']).exists():
            milestone = Milestone.objects.get(id=json_data['milestone_id'])
            pull.milestone = milestone
            pull.save()
        id = response.json()['id']
        pull.gitea_id = id
        pull.mergable = response.json()['mergeable']
        pull.save()
        return Response({'id': id}, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def get_all(request, repository_name):
    requests = PullRequest.objects.filter(project__name=repository_name)
    result = []
    for req in requests:
        obj = {
            'title': req.title, 'status': req.status, 'timestamp': req.timestamp, 'author': req.author.user.username, 'id': req.id,
            'labels': [], 'reviews': []
        }
        if req.milestone is not None:
            obj['milestone'] = req.milestone.title
        if req.assignee is not None:
            obj['assignee'] = {
                'username': req.assignee.user.username,
                'avatar': get_dev_avatar(req.assignee.user.username)
            }
        result.append(obj)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def get_one(request, repository_name, pull_id):
    
    # *** Basic data
    if not PullRequest.objects.filter(project__name=repository_name, gitea_id=pull_id).exists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(gitea_id=pull_id)
    result = {
        'title': req.title, 'status': req.status, 'timestamp': req.timestamp, 'author': {'username': req.author.user.username}, 'id': req.id,
        'labels': [], 'reviews': [], 'reviewers': [], 'mergeable': req.mergable, 'base': req.target.name, 'compare': req.source.name, 
        'commits': [], 'conflicting_files': []
    }
    if req.milestone is not None:
        result['milestone'] = {'id': req.milestone.id, 'title': req.milestone.title}
    if req.assignee is not None:
        result['assignee'] = {'username': req.assignee.user.username, 'avatar': get_dev_avatar(req.assignee.user.username)}
    # ***
    
    # *** Commits data
    owner_username = WorksOn.objects.get(role=Role.OWNER, project__name=repository_name).developer.user.username
    response = gitea_service.get_pull_request_commits(owner_username, repository_name, pull_id)

    commits_list_json = response.json()
    for commit_data in commits_list_json:
        result['commits'].append({
            'hash': commit_data['sha'],
            'message': commit_data['commit']['message'],
            'timestamp': commit_data['created'],
            'author': {'username': commit_data['author']['login'], 'avatar': get_dev_avatar(commit_data['author']['login'])},
            'files': commit_data['files'],
            'stats': commit_data['stats']
        })
    # ***

    # *** Diff
    response = gitea_service.get_pull_request_diff(owner_username, repository_name, pull_id)
    diff, overall_additions, overall_deletions = parse_diff(response.text)
    result['diff'] = diff
    result['overall_additions'] = overall_additions
    result['overall_deletions'] = overall_deletions
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def get_possible_assignees(request, repository_name):
    result = []
    works_on_list = WorksOn.objects.filter(project__name=repository_name)
    for obj in works_on_list:
        if obj.role != Role.IS_BANNED:
            result.append({'username': obj.developer.user.username, 'avatar': get_dev_avatar(obj.developer.user.username)})
    return Response(result, status=status.HTTP_200_OK)


def get_dev_avatar(username):
    developer = Developer.objects.get(user__username=username)
    if developer.avatar is None:
        gitea_user_info = gitea_service.get_gitea_user_info_gitea_service(username)
        return gitea_user_info['avatar_url']
    avatar_filename = developer.avatar.split('/')[1]
    return f"http://localhost/avatars/{avatar_filename}"


def parse_diff(diff_text):
    patch_set = PatchSet(StringIO(diff_text))
    diff = []
    overall_additions = 0
    overall_deletions = 0
    for patched_file in patch_set:
        file_path = patched_file.path
        overall_additions += patched_file.added
        overall_deletions += patched_file.removed
        lines = []
        for hunk in patched_file:
            for line in hunk:
                lines.append(str(line))
        diff.append({
            'file_path': file_path,
            'content': lines,
            'additions': patched_file.added,
            'deletions': patched_file.removed
        })
    return diff, overall_additions, overall_deletions