import threading

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from datetime import datetime

from main.models import Comment, Issue, Milestone, PullRequest, Developer, Label, Project


class LabelSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=255)
    description = serializers.CharField(required=True, allow_blank=True, max_length=255)

    def create(self, validated_data):
        project_name = self.context.get('request').parser_context.get('kwargs').get('repository_name', None)
        if project_name is None:
            raise Http404()
        try:
            project = Project.objects.get(name=project_name)
            name = validated_data['name']
            description = validated_data['description']

            if self.duplicate_label_exists(name):
                raise Http404()
            label = Label.objects.create(name=name, description=description, project=project)
            return label
        except ObjectDoesNotExist:
            raise Http404()

    def duplicate_label_exists(self, name):
        if Label.objects.filter(name=name).exists():
            return True
        return False
