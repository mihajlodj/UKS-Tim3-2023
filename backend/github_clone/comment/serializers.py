import threading

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from datetime import datetime

from main.models import Comment, Issue, Milestone, PullRequest, Developer

# from main.gitea_service import function


class CommentSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, allow_blank=False, max_length=500)
    parent = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    type_for = serializers.CharField(required=False, allow_blank=True)    # issue, milestone, pull_request what is this comment for
    type_id = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data):
        created_by_username = self.context['request'].auth.get('username', None)
        if created_by_username is None:
            raise Http404()
        type_for = validated_data['type_for']
        is_type_for_valid = self.valid_type_for(type_for)
        if not is_type_for_valid:
            raise Http404()
        try:
            # check if type_id object exists based on id
            type_id = validated_data['type_id']
            type_id_object_exists = self.check_if_type_id_object_exists(type_id, type_for)
            if not type_id_object_exists:
                raise Http404()
            parent_id_param = validated_data['parent']
            # find parent comment with id
            parent_comment = self.try_find_parent_comment(parent_id_param)

            developer = Developer.objects.get(user__username=created_by_username)

            # create comment object
            comment = Comment.objects.create(content=validated_data['content'],
                                             parent=parent_comment,
                                             caused_by=developer)
            # add issue, milestone or pull_request and save it
            comment = self.add_attached_type(comment, type_id, type_for)
            comment.save()
            return comment
        except ObjectDoesNotExist:
            raise Http404()

    def valid_type_for(self, type_for):
        if type_for == "issue":
            return True
        elif type_for == "milestone":
            return True
        elif type_for == "pull_request":
            return True
        return False

    def check_if_type_id_object_exists(self, type_id, type_for):
        if type_for == "issue":
            return self.check_if_issue_exists(type_id)
        elif type_for == "milestone":
            return self.check_if_milestone_exists(type_id)
        elif type_for == "pull_request":
            return self.check_if_pull_request_exists(type_id)
    def check_if_issue_exists(self, type_id):
        if Issue.objects.filter(id=type_id).exists():
            return True
        return False

    def check_if_milestone_exists(self, type_id):
        if Milestone.objects.filter(id=type_id).exists():
            return True
        return False

    def check_if_pull_request_exists(self, type_id):
        if PullRequest.objects.filter(id=type_id).exists():
            return True
        return False

    def try_find_parent_comment(self, parent_id_param):
        if parent_id_param is None or parent_id_param == '':
            return None
        if not Comment.objects.filter(id=parent_id_param).exists():
            raise Http404()
        return Comment.objects.get(id=parent_id_param)

    def add_attached_type(self, comment, type_id, type_for):
        if type_for == "issue":
            return self.add_issue_on_comment(comment, type_id)
        elif type_for == "milestone":
            return self.add_milestone_on_comment(comment, type_id)
        elif type_for == "pull_request":
            return self.add_pull_request_on_comment(comment, type_id)

    def add_issue_on_comment(self, comment, type_id):
        issue = Issue.objects.get(id=type_id)
        comment.issue = issue
        return comment

    def add_milestone_on_comment(self, comment, type_id):
        milestone = Milestone.objects.get(id=type_id)
        comment.milestone = milestone
        return comment

    def add_pull_request_on_comment(self, comment, type_id):
        pull_request = PullRequest.objects.get(id=type_id)
        comment.pull_request = pull_request
        return comment
