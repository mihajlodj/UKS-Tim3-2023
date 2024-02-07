import threading

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from main.models import Project, WorksOn, Milestone, MilestoneState

from main.gitea_service import create_milestone, update_milestone


class MilestoneSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=False, max_length=255,
                                 validators=[RegexValidator(regex=r'^[a-zA-Z][\w-]*$', message="Invalid milestone title", code="invalid_milestone_title")])
    description = serializers.CharField(required=True, allow_blank=True, max_length=255)
    deadline = serializers.DateField(format='%Y-%m-%d')
    state = serializers.BooleanField(required=False)  # if true state is OPEN, if false state is CLOSED
    repo_name = serializers.CharField(required=False, allow_blank=False)

    def create(self, validated_data):
        project_name = self.context.get('request').parser_context.get('kwargs').get('repository_name', None)
        if project_name is None:
            raise Http404()
        try:
            project = Project.objects.get(name=project_name)
            owner = WorksOn.objects.get(role='Owner', project=project).developer.user.username

            if Milestone.objects.filter(title=validated_data['title'], project=project).exists():
                raise ParseError("duplicate title for milestone")

            milestone = Milestone.objects.create(title=validated_data['title'],
                                                 description=validated_data['description'],
                                                 state=MilestoneState.OPEN,
                                                 deadline=validated_data['deadline'],
                                                 project=project)

            #threading.Thread(target=self.gitea_create_milestone, args=([owner, project_name, milestone]), kwargs={}).start()
            gitea_milestone_id = self.gitea_create_milestone(owner, project_name, milestone)
            milestone.id_from_gitea = gitea_milestone_id
            milestone.save()
            return milestone
        except ObjectDoesNotExist:
            raise Http404()

    def update(self, instance, validated_data):
        project_name = validated_data.get('repo_name')
        print(project_name)
        if project_name is None:
            raise Http404()
        try:
            project = Project.objects.get(name=project_name)
            owner = WorksOn.objects.get(role='Owner', project=project).developer.user.username

            new_title = validated_data.get('title', instance.title)
            if not Milestone.objects.filter(title=new_title, project=project).exists():
                instance.title = new_title
            instance.description = validated_data.get('description', instance.description)
            instance.deadline = validated_data.get('deadline', instance.deadline)

            new_state = validated_data.get('state', instance.state)
            if new_state != instance.state:
                instance.state = new_state

            instance.save()

            # update gitea
            threading.Thread(target=self.gitea_update_milestone, args=([owner, project_name, instance]),
                             kwargs={}).start()
            return instance
        except ObjectDoesNotExist:
            raise Http404()

    def gitea_create_milestone(self, owner, repository_name, milestone):
        return create_milestone(owner, repository_name, milestone)

    def gitea_update_milestone(self, owner, repository_name, milestone):
        update_milestone(owner, repository_name, milestone)
