from main.models import Watches, WatchOption, Notification

def send_notification_pull_request_created(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_people_to_notify_for_pr(repository, pr_info)
    notification_msg = f'@{pr_info['initiated_by']} opened new pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']}) -> {pr_info['dest']} for repository {repository_name}'
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_pull_request_merged(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_people_to_notify_for_pr(repository, pr_info)
    notification_msg = f'@{pr_info['initiated_by']} merged pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}'
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_pull_request_closed(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_people_to_notify_for_pr(repository, pr_info)
    notification_msg = f'@{pr_info['initiated_by']} closed pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}'
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def send_notification_pull_request_reopened(owner_username, repository, pr_info):
    repository_name = f'@{owner_username}/{repository.name}'
    receivers = find_people_to_notify_for_pr(repository, pr_info)
    notification_msg = f'@{pr_info['initiated_by']} reopened pull request: {pr_info['title']} #{pr_info['id']} ({pr_info['src']} -> {pr_info['dest']}) for repository {repository_name}'
    for receiver in receivers:
        send_notification(receiver, notification_msg)


def find_people_to_notify_for_pr(repository, pr_info):
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
    

def send_notification(username, message):
    print(f'Sending notification to {username}')
    Notification.objects.create(sent_to=username, message=message)
