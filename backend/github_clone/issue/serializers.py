from django.http import JsonResponse
from rest_framework import serializers

from main.models import Issue, Developer, Project, WorksOn
from main.gitea_service import create_issue, get_issues, update_issue, delete_issue


class IssueSerializer(serializers.Serializer):
    title = serializers.CharField(
        required=True,
        max_length=30,
    )
    description = serializers.CharField(
        max_length=255,
    )
    # created = serializers.DateTimeField()
    # manager = DeveloperSerializer()
    manager = serializers.CharField(allow_blank=False)
    project = serializers.CharField(allow_blank=False)
    milestone = serializers.CharField(allow_blank=True)
    def create(self, validated_data):
        issue = Issue.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            project=Project.objects.get(name=validated_data['project']),
            manager=Developer.objects.get(user__username=validated_data['manager']),
            tags=[]
        )
        # issue = Issue()
        # issue.title = validated_data['title']
        # issue.description = validated_data['description']
        # issue.project = Project.objects.get(name=validated_data['project'])
        # issue.manager = Developer.objects.get(user__username=validated_data['manager'])

        # issue.save()  # nisam siguran dal treba ovo
        owner = WorksOn.objects.get(role='Owner', project=issue.project).developer.user.username
        create_issue(owner=owner, repo=issue.project.name, issue=issue)
        return serialize_issue(issue)
        # return issue

def serialize_issue(issue):
    return {
        'title': issue.title,
        'description': issue.description,
        'open': issue.open,
        'created': str(issue.created),
        'manager': issue.manager.user.username,
        'project': issue.project.name,
        'milestone': serialize_milestone(issue),
        'tags': serialize_label_tags(issue)
    }

def serialize_milestone(issue):
    if issue.milestone is None:
        return ''
    return issue.milestone.title

def serialize_label_tags(issue):
    if issue.tags is None or issue.tags == []:
        return []
    return [tag.name for tag in issue.tags]