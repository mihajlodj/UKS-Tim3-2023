from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class AccessModifiers(models.TextChoices):
    PRIVATE = 'Private', 'Private'
    PUBLIC = 'Public', 'Public'


class Role(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    UNREGISTERED = 'Unregistered', 'Unregistered'
    REPORTER = 'Reporter', 'Reporter'
    DEVELOPER = 'Developer', 'Developer'
    MAINTAINER = 'Maintainer', 'Maintainer'
    OWNER = 'Owner', 'Owner'
    IS_BANNED = 'IsBanned', 'IsBanned'


class Event(models.Model):
    time = models.DateTimeField(default=timezone.now)
    caused_by = models.ForeignKey('main.Developer', related_name='caused_events', on_delete=models.CASCADE)
    issue = models.ForeignKey('main.Issue', related_name='events', on_delete=models.CASCADE)
    milestone = models.ForeignKey('main.Milestone', related_name='events', on_delete=models.CASCADE)

    # class Meta:
    #     abstract = True


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    assignment = models.ForeignKey('Assignment', related_name='developers', on_delete=models.SET_NULL, null=True,
                                   blank=True)


class Assignment(models.Model):
    event = models.OneToOneField('main.Event', on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=255)
    developer = models.ForeignKey(Developer, related_name='tasks', on_delete=models.CASCADE)
    issue = models.ForeignKey('Issue', related_name='contains', on_delete=models.CASCADE)


class Issue(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    manager = models.ForeignKey(Developer, related_name='managed_issues', on_delete=models.SET_NULL, null=True,
                                blank=True)
    milestone = models.ForeignKey('Milestone', related_name='issues', on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=255)
    access_modifier = models.CharField(max_length=10, choices=AccessModifiers.choices,
                                       default=AccessModifiers.PUBLIC)
    developers = models.ManyToManyField(Developer, through='WorksOn')


class Branch(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name='branches', on_delete=models.CASCADE, null=True, blank=True)
    default_branch_of_project = models.OneToOneField(Project, related_name='default_branch', on_delete=models.CASCADE,
                                                     null=True, blank=True)
    source = models.ForeignKey('self', related_name='branches', on_delete=models.CASCADE, null=True, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now)
    event = models.OneToOneField('main.Event', on_delete=models.CASCADE)


class Commit(models.Model):
    hash = models.CharField(max_length=255)
    author = models.ForeignKey(Developer, related_name='authored_commits', on_delete=models.CASCADE)
    committer = models.ForeignKey(Developer, related_name='committed_commits', on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, related_name='commits', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='commits')


class Milestone(models.Model):
    deadline = models.DateField()
    project = models.ForeignKey(Project, related_name='milestones', on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    event = models.OneToOneField('main.Event', on_delete=models.CASCADE)


class Reaction(models.Model):
    code = models.CharField(max_length=255)
    developer = models.ForeignKey(Developer, related_name='reactions', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='reactions', on_delete=models.CASCADE)


class ContentChanged(models.Model):
    new_content = models.TextField()
    changer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='changer')
    event = models.OneToOneField('main.Event', on_delete=models.CASCADE)


class WorksOn(models.Model):
    role = models.CharField(max_length=20, choices=AccessModifiers.choices)
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
    author = models.ForeignKey(Developer, related_name='pull_requests_author', on_delete=models.CASCADE)
    reviewers = models.ManyToManyField(Developer, related_name='pull_requests_reviewers')
