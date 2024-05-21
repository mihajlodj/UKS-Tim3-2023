import threading
from django.http import Http404
from main.models import PullRequest, Branch, PullRequestReviewer, Developer, Milestone, WorksOn, Role, Commit
import re
from developer import service as developer_service
from websocket import notification_service

def get_pull_title(json_data):
    if 'title' not in json_data:
        return json_data['compare']
    return json_data['title']

def save_pull_request(owner_username, author_username, repository_name, json_data, response):
    project = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).project
    author = Developer.objects.get(user__username=author_username)
    src = Branch.objects.get(name=json_data['compare'], project=project)
    dest = Branch.objects.get(name=json_data['base'], project=project)
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

    if 'reviewers' in json_data:
        print('Reviewers are in json data')
        for reviewer_username in json_data['reviewers']:
            if Developer.objects.filter(user__username=reviewer_username).exists():
                reviewer = Developer.objects.get(user__username=reviewer_username)
                PullRequestReviewer.objects.create(pull_request=pull, reviewer=reviewer)
    else:
        print(json_data)

    return pull.gitea_id


def update_commits_after_merge(pull):
    source = pull.source
    target = pull.target
    target_all_commits_hashes = set([commit.hash for commit in Commit.objects.filter(branch=target)])
    source_all_commits = Commit.objects.filter(branch=source)
    for commit in source_all_commits:
        if commit.hash not in target_all_commits_hashes:
            new_commit = Commit.objects.create(
                hash=commit.hash,
                author=commit.author,
                committer=commit.committer,
                branch=target,
                timestamp=commit.timestamp,
                message=commit.message,
                additional_description=commit.additional_description
            )
            if commit.tags:
                new_commit.tags.set(commit.tags.all())
            new_commit.save()


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

def update_assignee(json_data, req, owner_username, repository_name):
    if 'assignee_username' in json_data:
        project = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).project
        assignee_username = json_data['assignee_username']
        if not WorksOn.objects.filter(project=project, developer__user__username=assignee_username).exists():
            raise Http404()
        works_on = WorksOn.objects.get(project=project, developer__user__username=assignee_username)
        if works_on.role == Role.IS_BANNED:
            raise Http404()
        developer = Developer.objects.get(user__username=assignee_username)
        req.assignee = developer
    else:
        req.assignee = None
    req.save()
    return req

def update_reviewers(json_data, pull_request, owner_username, repository_name, request):
    if 'reviewers' not in json_data:
        return
    existing_reviewers = PullRequestReviewer.objects.filter(pull_request=pull_request)
    existing_reviewers_usernames = []
    for existing_reviewer in existing_reviewers:
        existing_reviewers_usernames.append(existing_reviewer.reviewer.user.username)
        existing_reviewer.delete()
    project = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).project
    for reviewer in json_data['reviewers']:
        if not WorksOn.objects.filter(project=project, developer__user__username=reviewer['username']).exists():
            raise Http404()
        works_on = WorksOn.objects.get(project=project, developer__user__username=reviewer['username'])
        if works_on.role == Role.IS_BANNED:
            raise Http404()
        developer = Developer.objects.get(user__username=reviewer['username'])
        PullRequestReviewer.objects.create(pull_request=pull_request, reviewer=developer)
        if reviewer['username'] not in existing_reviewers_usernames:
            pr_info = {'id': pull_request.gitea_id, 'title': pull_request.title, 'src': pull_request.source.name, \
                       'dest': pull_request.target.name, 'initiated_by': request.user.username}
            threading.Thread(target=notification_service.send_notification_pull_request_reviewer_added, args=([owner_username, project, pr_info, reviewer['username']]), kwargs={}).start()

def get_reviwers(pull_request):
    result = []
    for object in PullRequestReviewer.objects.filter(pull_request=pull_request):
        reviewer_username = object.reviewer.user.username
        result.append({'username': reviewer_username, 'avatar': developer_service.get_dev_avatar(reviewer_username)})
    return result


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
