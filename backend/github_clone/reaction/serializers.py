import threading

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from datetime import datetime
from websocket import notification_service

from main.models import Comment, Issue, Milestone, PullRequest, Developer, Reaction, WorksOn


class ReactionSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, allow_blank=False, max_length=255)
    comment_id = serializers.CharField(required=True, allow_blank=False, max_length=255)

    def create(self, validated_data):
        created_by_username = self.context['request'].auth.get('username', None)
        created_by_developer_id = self.context['request'].user.developer.id
        project_name = self.context.get('request').parser_context.get('kwargs').get('repository_name', None)
        owner_username = self.context.get('request').parser_context.get('kwargs').get('owner_username', None)
        try:
            works_on = WorksOn.objects.get(role='Owner', project__name=project_name,
                                           developer__user__username=owner_username)
            project = works_on.project
            owner = works_on.developer

            code = validated_data['code']
            developer = Developer.objects.get(id=created_by_developer_id)
            if developer is None:
                raise Http404()
            if created_by_username != developer.user.username:
                raise Http404()
            comment = Comment.objects.get(id=validated_data['comment_id'])

            if self.duplicate_reaction_exists(code, developer, comment):
                raise Http404()

            # Create and save Reaction
            reaction = Reaction.objects.create(code=code,
                                               developer=developer,
                                               comment=comment)

            reaction_info = {
                'creator': created_by_username,
                'comment_content': comment.content,
            }
            threading.Thread(target=notification_service.send_notification_reaction_added,
                             args=([owner.user.username, project, reaction_info]), kwargs={}).start()

            reaction.save()
            return reaction
        except ObjectDoesNotExist:
            raise Http404()

    def duplicate_reaction_exists(self, code, developer, comment):
        if Reaction.objects.filter(code=code, developer=developer, comment=comment).exists():
            return True
        return False
