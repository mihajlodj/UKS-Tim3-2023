import threading
from main.models import Developer, Watches, WatchOption, Notification
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_notification_pull_request_created(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_receivers_for_pr_status_changed(repository, pr_info)
    notification_msg = f'@{pr_info['initiated_by']} opened new pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']}) -> {pr_info['dest']} for repository {repository_name}'
    for receiver in receivers:
        send_notification(receiver, notification_msg)
    for reviewer in pr_info['reviewers']:
        send_notification_pull_request_reviewer_added(owner_username, repository, pr_info, reviewer)


def send_notification_pull_request_merged(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_receivers_for_pr_status_changed(repository, pr_info)
    notification_msg = f'@{pr_info['initiated_by']} merged pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}'
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
    notification_msg = f'@{pr_info['initiated_by']} closed pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}'
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_pull_request_reopened(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_receivers_for_pr_status_changed(repository, pr_info)
    notification_msg = f'@{pr_info['initiated_by']} reopened pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}'
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_pull_request_changed_assignee(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    new_assignee = pr_info['assignee']
    if new_assignee == pr_info['initiated_by'] or (Watches.objects.filter(developer__user__username=new_assignee, project=repository).exists() and \
        Watches.objects.get(developer__user__username=new_assignee, project=repository).option == WatchOption.IGNORE):
        return
    notification_msg_for_assignee = f'@{pr_info['initiated_by']} assigned you to pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}'
    send_notification(new_assignee, notification_msg_for_assignee)
    other_receivers = find_receivers_for_pr_assignee_changed(repository, pr_info)
    notification_msg_for_others = f'@{pr_info['initiated_by']} assigned {new_assignee} to pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}'
    for receiver in other_receivers:
        send_notification(receiver, notification_msg_for_others)


def send_notification_pull_request_reviewer_added(owner_username, repository, pr_info, reviewer_username):
    if Watches.objects.filter(developer__user__username=reviewer_username, project=repository).exists() and \
        Watches.objects.get(developer__user__username=reviewer_username, project=repository).option == WatchOption.IGNORE:
        return
    repository_name = f'@{owner_username}/{repository.name}'
    notification_msg = f'@{pr_info['initiated_by']} requested review for pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}'
    send_notification(reviewer_username, notification_msg)


def send_notification_default_branch_push(owner_username, repository, commit_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_receivers_for_default_branch_push(repository, commit_info['author'])
    notification_msg = f'@{commit_info['author']} pushed to {repository_name} ({commit_info['message']})'
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


def send_notification(username, message):
    print(f'Sending notification to {username}')
    Notification.objects.create(sent_to=username, message=message)
    recipient = Developer.object.get(user__username=username).user.email
    threading.Thread(target=send_email, args=([message, recipient]), kwargs={}).start()


def send_email(message, recipient):
        subject = '[Github Clone] You have a new notification'
        html_message = render_to_string('notification_email.html', {'message': message})
        plain_message = strip_tags(html_message)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [recipient,]
        send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
