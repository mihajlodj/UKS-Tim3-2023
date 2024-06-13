import threading

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from datetime import datetime
from websocket import notification_service

from main.models import Comment, Issue, Milestone, PullRequest, Developer, Label, Project, WorksOn


class LabelSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=255)
    description = serializers.CharField(required=True, allow_blank=True, max_length=255)

    def create(self, validated_data):
        project_name = self.context.get('request').parser_context.get('kwargs').get('repository_name', None)
        owner_username = self.context.get('request').parser_context.get('kwargs').get('owner_username', None)
        label_creator = self.context.get('request').user.username
        if project_name is None:
            raise Http404()
        try:
            works_on = WorksOn.objects.get(role='Owner', project__name=project_name, developer__user__username=owner_username)
            owner = works_on.developer

            project = Project.objects.get(name=project_name)
            name = validated_data['name']
            description = validated_data['description']

            if self.duplicate_label_exists(name):
                raise Http404()
            label = Label.objects.create(name=name, description=description, project=project)

            label_info = {
                'creator': label_creator,
                'label_name': label.name,
            }
            return label
        except ObjectDoesNotExist:
            raise Http404()

    def update(self, instance, validated_data):
        project_name = self.context.get('request').parser_context.get('kwargs').get('repository_name', None)
        owner_username = self.context.get('request').parser_context.get('kwargs').get('owner_username', None)
        label_creator = self.context.get('request').user.username

        label_id = self.context.get('request').parser_context.get('kwargs').get('id', None)
        if label_id is None or not label_id.isdigit():
            raise Http404()
        try:
            works_on = WorksOn.objects.get(role='Owner', project__name=project_name,
                                           developer__user__username=owner_username)
            owner = works_on.developer
            project = Project.objects.get(name=project_name)

            new_name = validated_data.get('name', instance.name)
            new_description = validated_data.get('description', instance.description)
            if not (len(new_name) == 0) and not self.duplicate_label_exists(new_name):
                instance.name = new_name
            instance.description = new_description

            instance.save()
            return instance
        except ObjectDoesNotExist:
            raise Http404()

    def duplicate_label_exists(self, name):
        if Label.objects.filter(name=name).exists():
            return True
        return False
