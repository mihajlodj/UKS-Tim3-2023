import threading
from main.models import Developer, Watches, WatchOption, Notification
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_notification_pull_request_created(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_receivers_for_pr_status_changed(repository, pr_info)
    notification_msg = f"@{pr_info['initiated_by']} opened new pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']}) -> {pr_info['dest']} for repository {repository_name}"
    for receiver in receivers:
        send_notification(receiver, notification_msg)
    for reviewer in pr_info['reviewers']:
        send_notification_pull_request_reviewer_added(owner_username, repository, pr_info, reviewer)


def send_notification_pull_request_merged(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_receivers_for_pr_status_changed(repository, pr_info)
    notification_msg = f"@{pr_info['initiated_by']} merged pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}"
    for receiver in receivers:
        send_notification(receiver, notification_msg)
    if repository.default_branch.name == pr_info['dest']:
        receivers_for_default_branch_push = find_receivers_for_default_branch_push(repository, pr_info['initiated_by'])
        for receiver in receivers_for_default_branch_push:
            if receiver not in receivers:
                send_notification(receiver, notification_msg)


def send_notification_pull_request_closed(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_receivers_for_pr_status_changed(repository, pr_info)
    notification_msg = f"@{pr_info['initiated_by']} closed pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}"
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_pull_request_reopened(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_receivers_for_pr_status_changed(repository, pr_info)
    notification_msg = f"@{pr_info['initiated_by']} reopened pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}"
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_pull_request_changed_assignee(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    new_assignee = pr_info['assignee']

    if not (new_assignee == pr_info['initiated_by'] or (Watches.objects.filter(developer__user__username=new_assignee, project=repository).exists() and \
        Watches.objects.get(developer__user__username=new_assignee, project=repository).option == WatchOption.IGNORE)):
        notification_msg_for_assignee = f"@{pr_info['initiated_by']} assigned you to pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}"
        send_notification(new_assignee, notification_msg_for_assignee)
    other_receivers = find_receivers_for_pr_assignee_changed(repository, pr_info)
    notification_msg_for_others = f"@{pr_info['initiated_by']} assigned {new_assignee} to pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}"
    for receiver in other_receivers:
        if receiver != new_assignee:
            send_notification(receiver, notification_msg_for_others)


def send_notification_pull_request_reviewer_added(owner_username, repository, pr_info, reviewer_username):
    if reviewer_username == pr_info['initiated_by'] or (Watches.objects.filter(developer__user__username=reviewer_username, project=repository).exists() and \
        Watches.objects.get(developer__user__username=reviewer_username, project=repository).option == WatchOption.IGNORE):
        return
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"@{pr_info['initiated_by']} requested review for pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}"
    send_notification(reviewer_username, notification_msg)


def send_notification_default_branch_push(owner_username, repository, commit_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_receivers_for_default_branch_push(repository, commit_info['author'])
    notification_msg = f"@{commit_info['author']} pushed to {repository_name} ({commit_info['message']})"
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_repository_starred(owner_username, repository, starred_by):
    if (starred_by == owner_username):
        return
    if Watches.objects.filter(developer__user__username=owner_username, project=repository).exists() and \
        Watches.objects.get(developer__user__username=owner_username, project=repository).option == WatchOption.IGNORE:
        return
    notification_msg = f'@{starred_by} starred your repository: @{owner_username}/{repository.name}'
    send_notification(owner_username, notification_msg)


def find_receivers_for_pr_status_changed(repository, pr_info):
    receivers = []
    watches = Watches.objects.filter(project=repository)
    for watch in watches:
        dev_username = watch.developer.user.username
        if dev_username == pr_info['initiated_by'] or watch.option == WatchOption.IGNORE:
            continue
        if watch.option == WatchOption.ALL or watch.pull_events or \
            (watch.option == WatchOption.PARTICIPATING and (dev_username == pr_info['author'] or dev_username == pr_info['assignee'] or dev_username in pr_info['reviewers'])):
            receivers.append(dev_username)
    return receivers
    
def find_receivers_for_pr_assignee_changed(repository, pr_info):
    receivers = []
    watches = Watches.objects.filter(project=repository)
    for watch in watches:
        dev_username = watch.developer.user.username
        if dev_username == pr_info['initiated_by'] or watch.option == WatchOption.IGNORE:
            continue
        if watch.option == WatchOption.ALL or watch.pull_events or \
            (watch.option == WatchOption.PARTICIPATING and dev_username in pr_info['reviewers']):
            receivers.append(dev_username)
    return receivers

def find_receivers_for_default_branch_push(repository, author):
    receivers = []
    watches = Watches.objects.filter(project=repository)
    for watch in watches:
        dev_username = watch.developer.user.username
        if dev_username != author and watch.option == WatchOption.ALL:
            receivers.append(dev_username)
    return receivers


def find_receivers_for_release_events(release):
    receivers = []
    watches = Watches.objects.filter(project=release.project)
    for watch in watches:
        dev_username = watch.developer.user.username
        if watch.option == WatchOption.ALL or (watch.option == WatchOption.PARTICIPATING and watch.release_events):
            receivers.append(dev_username)
    return receivers

def find_receivers_for_issue_events(issue):
    receivers = []
    watches = Watches.objects.filter(project=issue.project)
    for watch in watches:
        dev_username = watch.developer.user.username
        if watch.option == WatchOption.ALL or (watch.option == WatchOption.PARTICIPATING and watch.issue_events) or \
            (watch.option == WatchOption.PARTICIPATING and dev_username == issue.creator.user.username):
            receivers.append(dev_username)
    return receivers


def send_notification_milestone_created(owner_username, repository, milestone_info):
    if owner_username == milestone_info['creator']:
        return
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{milestone_info['creator']} created milestone {milestone_info['title']} for repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_milestone_edited(owner_username, repository, milestone_info):
    if owner_username == milestone_info['creator']:
        return
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{milestone_info['creator']} edited milestone {milestone_info['title']} for repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_milestone_deleted(owner_username, repository, milestone_info):
    if owner_username == milestone_info['creator']:
        return
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{milestone_info['creator']} deleted milestone {milestone_info['title']} for repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_milestone_closed(owner_username, repository, milestone_info):
    if owner_username == milestone_info['creator']:
        return
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{milestone_info['creator']} closed milestone {milestone_info['title']} for repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_milestone_reopened(owner_username, repository, milestone_info):
    if owner_username == milestone_info['creator']:
        return
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{milestone_info['creator']} reopened milestone {milestone_info['title']} for repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_comment_created(owner_username, repository, comment_info):
    repository_name = f'@{owner_username}/{repository.name}'
    type_for = comment_info['type_for']
    notification_msg = f"{comment_info['creator']} commented on {type_for} #{comment_info['type_id']} for repository {repository_name}"
    watches = Watches.objects.filter(project=repository)
    if type_for == 'issue':
        for watch in watches:
            dev_username = watch.developer.user.username
            if watch.option == WatchOption.IGNORE or dev_username == comment_info['creator']:
                continue
            if watch.option == WatchOption.ALL or watch.issue_events or (watch.option == WatchOption.PARTICIPATING and dev_username in comment_info['participants']):
                send_notification(dev_username, notification_msg)
    elif type_for == 'pull_request':
        for watch in watches:
            dev_username = watch.developer.user.username
            if watch.option == WatchOption.IGNORE or dev_username == comment_info['creator']:
                continue
            if watch.option == WatchOption.ALL or watch.pull_events or (watch.option == WatchOption.PARTICIPATING and dev_username in comment_info['participants']):
                send_notification(dev_username, notification_msg)


def send_notification_review_for_pr_added(owner_username, repository, review_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{review_info['creator']} added review for PR {review_info['pr_title']} #{review_info['pr_id']} for repository {repository_name}"
    for watch in Watches.objects.filter(project=repository):
        dev_username = watch.developer.user.username
        if dev_username == review_info['creator'] or watch.option == WatchOption.IGNORE:
            continue
        if dev_username == review_info['pr_author'] or dev_username == review_info['pr_assignee'] or dev_username in review_info['pr_reviewers']:
            send_notification(dev_username, notification_msg)


def send_notification_label_added_on_issue(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} added label {label_info['label_name']} to issue {label_info['joined_entity_name']} for repository {repository_name}"
    receivers = find_receivers_issue_labeled(repository, label_info)
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_label_removed_from_issue(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} removed label {label_info['label_name']} from issue {label_info['joined_entity_name']} for repository {repository_name}"
    receivers = find_receivers_issue_labeled(repository, label_info)
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_label_added_on_pull_request(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} added label {label_info['label_name']} to pull request {label_info['joined_entity_name']} for repository {repository_name}"
    receivers = find_receivers_pull_request_labeled(repository, label_info)
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_label_removed_from_pull_request(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} removed label {label_info['label_name']} from pull_request {label_info['joined_entity_name']} for repository {repository_name}"
    receivers = find_receivers_pull_request_labeled(repository, label_info)
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def find_receivers_issue_labeled(repository, label_info):
    receivers = []
    watches = Watches.objects.filter(project=repository)
    for watch in watches:
        dev_username = watch.developer.user.username
        if dev_username == label_info['creator'] or watch.option == WatchOption.IGNORE:
            continue
        if watch.option == WatchOption.ALL or watch.issue_events or \
            (watch.option == WatchOption.PARTICIPATING and (dev_username == label_info['issue_creator'])):
            receivers.append(dev_username)
    return receivers


def find_receivers_pull_request_labeled(repository, label_info):
    receivers = []
    watches = Watches.objects.filter(project=repository)
    for watch in watches:
        dev_username = watch.developer.user.username
        if dev_username == label_info['creator'] or watch.option == WatchOption.IGNORE:
            continue
        if watch.option == WatchOption.ALL or watch.pull_events or \
            (watch.option == WatchOption.PARTICIPATING and (dev_username == label_info['pr_author'] or dev_username == label_info['pr_assignee'] or dev_username in label_info['pr_reviewers'])):
            receivers.append(dev_username)
    return receivers


def send_notification_reaction_added(owner_username, repository, reaction_info):
    if reaction_info['creator'] == reaction_info['comment_creator']:
        return
    if Watches.objects.filter(project=repository, developer__user__username=reaction_info['comment_creator']).exists():
        watch = Watches.objects.get(project=repository, developer__user__username=reaction_info['comment_creator'])
        if watch.option == WatchOption.IGNORE:
            return
        repository_name = f'@{owner_username}/{repository.name}'
        notification_msg = f"@{reaction_info['creator']} added reaction on your comment ({reaction_info['comment_content']}) you created in repository {repository_name}"
        send_notification(owner_username, notification_msg)


def send_notification_release_created(release, initiated_by):
    receivers = find_receivers_for_release_events(release)
    version = release.title + '.' + release.tag.name
    project_name = release.project.name
    release = 'full release' if release.pre_release is False else 'pre-release'
    notification_msg = f'Project {project_name} has released a new {release} version of the software: {version}'
    for receiver in receivers:
        if receiver != initiated_by:
            send_notification(receiver, notification_msg)


def send_notification_issue_created(issue, initiated_by):
    receivers = find_receivers_for_issue_events(issue)
    title = issue.title
    project_name = issue.project.name
    description = issue.description
    creator = issue.creator.user.username
    notification_msg = f'New issue created, by {creator}, for project {project_name}\n{title}\n{description}'
    for receiver in receivers:
        if receiver != initiated_by:
            send_notification(receiver, notification_msg)


def send_notification_issue_updated(issue, initiated_by):
    receivers = find_receivers_for_issue_events(issue)
    title = issue.title
    project_name = issue.project.name
    description = issue.description
    notification_msg = f'Issue {title} was updated, for project {project_name}\n{title}\n{description}'
    for receiver in receivers:
        if receiver != initiated_by:
            send_notification(receiver, notification_msg)


def send_notification_issue(issue, status, initiated_by):
    receivers = find_receivers_for_issue_events(issue)
    title = issue.title
    project_name = issue.project.name
    creator = issue.creator.user.username
    notification_msg = f'Issue {title}, by {creator}, for project {project_name} was {status}'
    for receiver in receivers:
        if receiver != initiated_by:
            send_notification(receiver, notification_msg)


def send_notification(username, message):
    print(f'Sending notification to {username}')
    Notification.objects.create(sent_to=username, message=message)
    recipient = Developer.objects.get(user__username=username).user.email
    threading.Thread(target=send_email, args=([message, recipient]), kwargs={}).start()


def send_email(message, recipient):
    subject = '[Github Clone] You have a new notification'
    html_message = render_to_string('notification_email.html', {'message': message})
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipient,]
    print(f'SENDING EMAIL: address {recipient}, message {message}...')
    send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
