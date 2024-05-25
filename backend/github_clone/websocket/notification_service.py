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
    print('HEREE')
    repository_name = f'@{owner_username}/{repository.name}'
    new_assignee = pr_info['assignee']
    if new_assignee == pr_info['initiated_by'] or (Watches.objects.filter(developer__user__username=new_assignee, project=repository).exists() and \
        Watches.objects.get(developer__user__username=new_assignee, project=repository).option == WatchOption.IGNORE):
        print('returning')
        return
    notification_msg_for_assignee = f"@{pr_info['initiated_by']} assigned you to pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}"
    send_notification(new_assignee, notification_msg_for_assignee)
    other_receivers = find_receivers_for_pr_assignee_changed(repository, pr_info)
    notification_msg_for_others = f"@{pr_info['initiated_by']} assigned {new_assignee} to pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}"
    for receiver in other_receivers:
        if receiver != new_assignee:
            send_notification(receiver, notification_msg_for_others)


def send_notification_pull_request_reviewer_added(owner_username, repository, pr_info, reviewer_username):
    if Watches.objects.filter(developer__user__username=reviewer_username, project=repository).exists() and \
        Watches.objects.get(developer__user__username=reviewer_username, project=repository).option == WatchOption.IGNORE:
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
            (watch.option == WatchOption.PARTICIPATING and (dev_username == pr_info['assignee'] or dev_username in pr_info['reviewers'])):
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


def send_notification_milestone_created(owner_username, repository, milestone_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{milestone_info['creator']} created milestone {milestone_info['title']} for repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_milestone_edited(owner_username, repository, milestone_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{milestone_info['creator']} edited milestone {milestone_info['title']} for repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_milestone_deleted(owner_username, repository, milestone_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{milestone_info['creator']} deleted milestone {milestone_info['title']} for repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_milestone_closed(owner_username, repository, milestone_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{milestone_info['creator']} closed milestone {milestone_info['title']} for repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_milestone_reopened(owner_username, repository, milestone_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{milestone_info['creator']} reopened milestone {milestone_info['title']} for repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_comment_created(owner_username, repository, comment_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{comment_info['creator']} commented on {comment_info['type_for']} #{comment_info['type_id']} you created for repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_label_created(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} created label {label_info['label_name']} for repository {repository_name}"
    receivers = find_receivers_for_label_events(repository, label_info['creator'])
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_label_updated(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} updated label {label_info['label_name']} for repository {repository_name}"
    receivers = find_receivers_for_label_events(repository, label_info['creator'])
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_label_deleted(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} deleted label {label_info['label_name']} for repository {repository_name}"
    receivers = find_receivers_for_label_events(repository, label_info['creator'])
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_label_added_on_milestone(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} added label {label_info['label_name']} to milestone {label_info['joined_entity_name']} for repository {repository_name}"
    receivers = find_receivers_for_label_events(repository, label_info['creator'])
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_label_removed_from_milestone(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} removed label {label_info['label_name']} from milestone {label_info['joined_entity_name']} for repository {repository_name}"
    receivers = find_receivers_for_label_events(repository, label_info['creator'])
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_label_added_on_issue(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} added label {label_info['label_name']} to issue {label_info['joined_entity_name']} for repository {repository_name}"
    receivers = find_receivers_for_label_events(repository, label_info['creator'])
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_label_removed_from_issue(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} removed label {label_info['label_name']} from issue {label_info['joined_entity_name']} for repository {repository_name}"
    receivers = find_receivers_for_label_events(repository, label_info['creator'])
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_label_added_on_pull_request(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} added label {label_info['label_name']} to pull request {label_info['joined_entity_name']} for repository {repository_name}"
    receivers = find_receivers_for_label_events(repository, label_info['creator'])
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_label_removed_from_pull_request(owner_username, repository, label_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"{label_info['creator']} removed label {label_info['label_name']} from pull_request {label_info['joined_entity_name']} for repository {repository_name}"
    receivers = find_receivers_for_label_events(repository, label_info['creator'])
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def find_receivers_for_label_events(repository, author):
    receivers = []
    watches = Watches.objects.filter(project=repository)
    for watch in watches:
        dev_username = watch.developer.user.username
        if dev_username != author and watch.option == WatchOption.ALL:
            receivers.append(dev_username)
    return receivers


def send_notification_reaction_added(owner_username, repository, reaction_info):
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f"@{reaction_info['creator']} added reaction on your comment ({reaction_info['comment_content']}) you created in repository {repository_name}"
    send_notification(owner_username, notification_msg)


def send_notification_release_created(release):
    receivers = find_receivers_for_release_events(release)
    version = release.title + '.' + release.tag.name
    project_name = release.project.name
    release = 'full release' if release.pre_release is False else 'pre-release'
    notification_msg = f'Project {project_name} has released a new {release} version of the software: {version}'
    for receiver in receivers:
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
