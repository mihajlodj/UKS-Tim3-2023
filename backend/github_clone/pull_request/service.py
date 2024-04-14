from django.http import Http404
from main.models import PullRequest, Branch, Project, Developer, Milestone, WorksOn, Role
import re
from developer import service as developer_service

def get_pull_title(json_data):
    if 'title' not in json_data:
        return json_data['compare']
    return json_data['title']

def save_pull_request(author_username, repository_name, json_data, response):
    author = Developer.objects.get(user__username=author_username)
    src = Branch.objects.get(name=json_data['compare'], project__name=repository_name)
    dest = Branch.objects.get(name=json_data['base'], project__name=repository_name)
    project = Project.objects.get(name=repository_name)   
    pull = PullRequest.objects.create(source=src, target=dest, project=project, author=author, title=get_pull_title(json_data), description=json_data['description'])
    if 'milestone_id' in json_data and Milestone.objects.filter(id=json_data['milestone_id']).exists():
        milestone = Milestone.objects.get(id=json_data['milestone_id'])
        pull.milestone = milestone
        pull.save()
    pull.gitea_id = response.json()['number']
    pull.mergeable = response.json()['mergeable']
    if 'assignee' in json_data and Developer.objects.filter(user__username=json_data['assignee']).exists():
        pull.assignee = Developer.objects.get(user__username=json_data['assignee'])
    pull.save()
    return pull.gitea_id

def update_milestone(json_data, req):
    if 'milestone_id' in json_data:
        milestone_id = json_data['milestone_id']
        if not Milestone.objects.filter(id=milestone_id).exists():
            raise Http404()
        milestone = Milestone.objects.get(id=milestone_id)
        req.milestone = milestone
    else:
        req.milestone = None
    req.save()

def update_assignee(json_data, req, repository_name):
    if 'assignee_username' in json_data:
        assignee_username = json_data['assignee_username']
        if not WorksOn.objects.filter(project__name=repository_name, developer__user__username=assignee_username).exists():
            raise Http404()
        works_on = WorksOn.objects.get(project__name=repository_name, developer__user__username=assignee_username)
        if works_on.role == Role.IS_BANNED:
            raise Http404()
        developer = Developer.objects.get(user__username=assignee_username)
        req.assignee = developer
    else:
        req.assignee = None
    req.save()

def get_pull_request_from_merge_commit(msg, repo_name):
    pattern = r'\(#(\d+)\)'
    matches = re.findall(pattern, msg)
    if matches:
        pull_id = int(matches[0])
        return PullRequest.objects.get(gitea_id=pull_id, project__name=repo_name)

def get_commit_author(username, msg, repo_name):
    if Developer.objects.filter(user__username=username).exists():
        return {'username': username, 'avatar': developer_service.get_dev_avatar(username)}
    req = get_pull_request_from_merge_commit(msg, repo_name)
    return {'username': req.merged_by.user.username, 'avatar': developer_service.get_dev_avatar(req.merged_by.user.username)}
