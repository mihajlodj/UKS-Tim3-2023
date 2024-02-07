import threading

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from main.models import Project, WorksOn, Milestone, MilestoneState

from main.gitea_service import create_milestone


class MilestoneSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=False, max_length=255,
                                 validators=[RegexValidator(regex=r'^[a-zA-Z][\w-]*$', message="Invalid milestone title", code="invalid_milestone_title")])
    description = serializers.CharField(required=True, allow_blank=True, max_length=255)
    deadline = serializers.DateField(format='%Y-%m-%d')

    def create(self, validated_data):
        project_name = self.context.get('request').parser_context.get('kwargs').get('repository_name', None)
        if project_name is None:
            raise Http404()
        try:
            project_name = self.context.get('request').parser_context.get('kwargs').get('repository_name', None)
            project = Project.objects.get(name=project_name)
            owner = WorksOn.objects.get(role='Owner', project=project).developer.user.username

            if Milestone.objects.filter(title=validated_data['title'], project=project).exists():
                raise ParseError("duplicate title for milestone")

            milestone = Milestone.objects.create(title=validated_data['title'],
                                                 description=validated_data['description'],
                                                 state=MilestoneState.OPEN,
                                                 deadline=validated_data['deadline'],
                                                 project=project)

            threading.Thread(target=self.gitea_create_milestone, args=([owner, project_name, milestone]), kwargs={}).start()
            return milestone
        except ObjectDoesNotExist:
            raise Http404()

    def gitea_create_milestone(self, owner, repository_name, milestone):
        create_milestone(owner, repository_name, milestone)
