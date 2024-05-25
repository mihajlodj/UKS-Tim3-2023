import threading

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ParseError


from websocket import notification_service
from main.models import WorksOn, Milestone, MilestoneState

from main.gitea_service import create_milestone, update_milestone


class MilestoneSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=False, max_length=255,
                                 validators=[RegexValidator(regex=r'^[a-zA-Z][\w-]*$', message="Invalid milestone title", code="invalid_milestone_title")])
    description = serializers.CharField(required=True, allow_blank=True, max_length=255)
    deadline = serializers.DateField(format='%Y-%m-%d')
    state = serializers.BooleanField(required=False)  # if true state is OPEN, if false state is CLOSED
    repo_name = serializers.CharField(required=False, allow_blank=False)

    def create(self, validated_data):
        created_by_username = self.context['request'].auth.get('username', None)
        project_name = self.context.get('request').parser_context.get('kwargs').get('repository_name', None)
        owner_username = self.context.get('request').parser_context.get('kwargs').get('owner_username', None)
        if project_name is None or owner_username is None:
            raise Http404()
        try:
            works_on = WorksOn.objects.get(role='Owner', project__name=project_name, developer__user__username=owner_username)
            project = works_on.project
            owner = works_on.developer

            if Milestone.objects.filter(title=validated_data['title'], project=project).exists():
                raise ParseError("duplicate title for milestone")

            milestone = Milestone.objects.create(title=validated_data['title'],
                                                 description=validated_data['description'],
                                                 state=MilestoneState.OPEN,
                                                 deadline=validated_data['deadline'],
                                                 project=project)

            #threading.Thread(target=self.gitea_create_milestone, args=([owner, project_name, milestone]), kwargs={}).start()
            gitea_milestone_id = self.gitea_create_milestone(owner_username, project_name, milestone)
            milestone.id_from_gitea = gitea_milestone_id
            milestone.save()
            milestone_info = {
                'creator': created_by_username,
                'title': milestone.title,
            }
            threading.Thread(target=notification_service.send_notification_milestone_created, args=([owner.user.username, project, milestone_info]), kwargs={}).start()
            return milestone
        except ObjectDoesNotExist:
            raise Http404()

    def update(self, instance, validated_data):
        created_by_username = self.context['request'].auth.get('username', None)
        project_name = validated_data.get('repo_name')
        owner_username = self.context.get('request').parser_context.get('kwargs').get('owner_username', None)
        print(project_name)
        if project_name is None or owner_username is None:
            raise Http404()
        try:
            works_on = WorksOn.objects.get(role='Owner', project__name=project_name, developer__user__username=owner_username)
            project = works_on.project
            owner = works_on.developer

            new_title = validated_data.get('title', instance.title)
            if not Milestone.objects.filter(title=new_title, project=project).exists():
                instance.title = new_title
            instance.description = validated_data.get('description', instance.description)
            instance.deadline = validated_data.get('deadline', instance.deadline)

            new_state_from_request = validated_data.get('state', instance.state)
            if new_state_from_request == True:
                new_state = MilestoneState.OPEN
            else:
                new_state = MilestoneState.CLOSED
            if new_state != instance.state:
                instance.state = new_state

            instance.save()
            milestone_info = {
                'creator': created_by_username,
                'title': instance.title,
            }
            threading.Thread(target=notification_service.send_notification_milestone_edited,
                             args=([owner.user.username, project, milestone_info]), kwargs={}).start()
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
