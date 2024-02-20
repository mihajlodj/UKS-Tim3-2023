from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils import timezone


class AccessModifiers(models.TextChoices):
    PRIVATE = 'Private', 'Private'
    PUBLIC = 'Public', 'Public'


class Role(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    UNREGISTERED = 'Unregistered', 'Unregistered'
    READONLY = 'Readonly', 'Readonly'
    DEVELOPER = 'Developer', 'Developer'
    MAINTAINER = 'Maintainer', 'Maintainer'
    OWNER = 'Owner', 'Owner'
    IS_BANNED = 'IsBanned', 'IsBanned'


class PullRequestStatus(models.TextChoices):
    OPEN = 'Open', 'Open'
    CLOSED = 'Closed', 'Closed'
    MERGED = 'Merged', 'Merged'


class MilestoneState(models.TextChoices):
    OPEN = 'Open', 'Open'
    CLOSED = 'Closed', 'Closed'


class Event(models.Model):
    time = models.DateTimeField(default=timezone.now)
    caused_by = models.ForeignKey('main.Developer', related_name='caused_events', on_delete=models.CASCADE)
    issue = models.ForeignKey('main.Issue', related_name='issue_events', on_delete=models.CASCADE, null=True)
    milestone = models.ForeignKey('main.Milestone', related_name='milestone_events', on_delete=models.CASCADE,
                                  null=True)
    pull_request = models.ForeignKey('main.PullRequest', related_name='pull_request_events', on_delete=models.CASCADE,
                                     null=True)


class SecondaryEmail(models.Model):
    developer = models.ForeignKey('Developer', on_delete=models.CASCADE)
    email = models.EmailField()
    primary = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gitea_token = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.CharField(max_length=1000, null=True, blank=True)


class Assignment(Event):
    developer = models.ForeignKey('Developer', related_name='assignments', on_delete=models.DO_NOTHING)
    # event = models.OneToOneField('main.Event', on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=255)
    developer = models.ForeignKey(Developer, related_name='tasks', on_delete=models.CASCADE)
    issue = models.ForeignKey('Issue', related_name='contains', on_delete=models.CASCADE)


class Issue(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    manager = models.ForeignKey(Developer, related_name='managed_issues', on_delete=models.DO_NOTHING, null=True,
                                blank=True)
    milestone = models.ForeignKey('Milestone', related_name='issues', on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    access_modifier = models.CharField(max_length=10, choices=AccessModifiers.choices, default=AccessModifiers.PUBLIC)
    default_branch = models.OneToOneField('Branch', related_name='default_branch', on_delete=models.CASCADE, null=True,
                                          blank=True)


class Branch(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name='branches', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='branches', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(Developer, related_name='branches', on_delete=models.CASCADE, null=True, blank=True)


class Tag(Event):
    name = models.CharField(max_length=255)
    # event = models.OneToOneField('main.Event', on_delete=models.CASCADE)


class Commit(models.Model):
    hash = models.CharField(max_length=255)
    author = models.ForeignKey(Developer, related_name='authored_commits', on_delete=models.CASCADE)
    committer = models.ForeignKey(Developer, related_name='committed_commits', on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, related_name='belongs_to', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='commits', blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField(null=True, blank=True)
    additional_description = models.TextField(null=True, blank=True)


class Milestone(models.Model):
    deadline = models.DateField()
    project = models.ForeignKey(Project, related_name='milestones', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="")
    description = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=10, choices=MilestoneState.choices, default=MilestoneState.OPEN)
    id_from_gitea = models.IntegerField(blank=True, null=True)


class Comment(Event):
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    # event = models.OneToOneField('main.Event', on_delete=models.CASCADE)


class Reaction(models.Model):
    code = models.CharField(max_length=255)
    developer = models.ForeignKey(Developer, related_name='reactions', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='reactions', on_delete=models.CASCADE)


class ContentChanged(Event):
    new_content = models.TextField()
    changer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='changer')
    # event = models.OneToOneField('main.Event', on_delete=models.CASCADE)


class WorksOn(models.Model):
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DEVELOPER)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Watches(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Fork(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Stars(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class PullRequest(models.Model):
    source = models.ForeignKey(Branch, related_name='pull_requests_source', on_delete=models.CASCADE)
    target = models.ForeignKey(Branch, related_name='pull_requests_target', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(Developer, related_name='pull_requests_author', on_delete=models.DO_NOTHING)
    assignee = models.ForeignKey(Developer, null=True, blank=True, related_name='pull_requests_assignee', on_delete=models.DO_NOTHING)
    milestone = models.ForeignKey(Milestone, related_name='pull_request_milestone', null=True, on_delete=models.DO_NOTHING)
    reviewers = models.ManyToManyField(Developer, related_name='pull_requests_reviewers', blank=True)
    status = models.CharField(max_length=10, choices=PullRequestStatus.choices, default=PullRequestStatus.OPEN)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    gitea_id = models.IntegerField(null=True)
    mergable = models.BooleanField(null=True)


class RegistrationCandidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
