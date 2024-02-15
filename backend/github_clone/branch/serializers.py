import threading
from django.http import Http404, HttpResponseBadRequest
from rest_framework import serializers
from django.core.validators import RegexValidator
from rest_framework.exceptions import ParseError
from main.gitea_service import create_branch
from main.models import Project, Branch, Developer, WorksOn
from django.core.exceptions import ObjectDoesNotExist


class BranchSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=255, 
                                 validators=[RegexValidator(regex=r'^[a-zA-Z][\w-]*$', message="Invalid branch name", code="invalid_branch_name")])
    parent = serializers.CharField(required=True, allow_blank=False, max_length=255)

    def create(self, validated_data):
        project_name = self.context.get('request').parser_context.get('kwargs').get('repository_name', None)
        created_by_username = self.context['request'].auth.get('username', None)
        if project_name is None or created_by_username is None:
            raise Http404()
        try:
            project = Project.objects.get(name=project_name)
            created_by = Developer.objects.get(user__username=created_by_username)
            owner = WorksOn.objects.get(role='Owner', project=project).developer.user.username
            parent = Branch.objects.get(name=validated_data['parent'], project=project)
            if Branch.objects.filter(name=validated_data['name'], project=project).exists():
               raise ParseError("duplicate branch name") 
            branch = Branch.objects.create(name=validated_data['name'], project=project, parent=parent, created_by=created_by)
            threading.Thread(target=self.gitea_create_branch, args=([owner, project_name, branch]), kwargs={}).start()
            return branch
        except ObjectDoesNotExist:
            raise Http404()

    def gitea_create_branch(self, owner, repository_name, branch):
        create_branch(owner, repository_name, branch)
