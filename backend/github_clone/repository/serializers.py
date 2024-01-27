import threading
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from main.gitea_service import create_repository
from main.models import Project, AccessModifiers, Branch, WorksOn, Developer


class RepositorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=255, 
                                 validators=[UniqueValidator(queryset=Project.objects.all()), 
                                             RegexValidator(regex=r'^[a-zA-Z][\w-]*$', message="Invalid repository name", code="invalid_repo_name")])
    description = serializers.CharField(required=False, allow_blank=True)
    access_modifier = serializers.ChoiceField(choices=AccessModifiers, default='Public')
    default_branch_name = serializers.CharField(required=False, allow_blank=True, max_length=255)

    def create(self, validated_data):
        branch_name = 'main'
        if 'default_branch_name' in validated_data and validated_data['default_branch_name'] != '':
            branch_name = validated_data['default_branch_name']
        project = Project.objects.create(name=validated_data['name'], description=validated_data['description'], access_modifier=validated_data['access_modifier'], default_branch=None)
        default_branch = Branch.objects.create(name=branch_name, project=project, parent=None)
        project.default_branch = default_branch
        project.save()
        username = self.context['request'].auth.get('username', None)
        WorksOn.objects.create(role="Owner", project=project, developer=Developer.objects.get(user__username=username))
        threading.Thread(target=self.gitea_create, args=([project, branch_name, username]), kwargs={}).start()
        return project

    def gitea_create(self, project, branch_name, username):
        description = ''
        if project.description is not None:
            description = project.description
        private = True
        if (project.access_modifier == "Public"):
            private = False
        create_repository({
            'default_branch': branch_name,
            'description': description,
            'name': project.name,
            'private': private
        }, username)
    