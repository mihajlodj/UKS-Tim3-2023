import threading
from django.http import Http404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

from main import gitea_service
from main.gitea_service import create_repository, update_repository
from main.models import Project, AccessModifiers, Branch, WorksOn, Developer
from django.contrib.auth.models import User


class RepositorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=255, 
                                 validators=[UniqueValidator(queryset=Project.objects.all()), 
                                             RegexValidator(regex=r'^[a-zA-Z][\w-]*$', message="Invalid repository name", code="invalid_repo_name")])
    description = serializers.CharField(required=False, allow_blank=True)
    access_modifier = serializers.ChoiceField(choices=AccessModifiers, default='Public')
    default_branch_name = serializers.CharField(required=False, allow_blank=True, max_length=255,
                                                validators=[RegexValidator(regex=r'^[a-zA-Z][\w-]*$', message="Invalid branch name", code="invalid_branch_name")])

    def create(self, validated_data):
        branch_name = 'main'
        if 'default_branch_name' in validated_data and validated_data['default_branch_name'] != '':
            branch_name = validated_data['default_branch_name']
        username = self.context['request'].auth.get('username', None)
        developer = Developer.objects.get(user__username=username)
        project = Project.objects.create(name=validated_data['name'], description=validated_data['description'], access_modifier=validated_data['access_modifier'], default_branch=None)
        default_branch = Branch.objects.create(name=branch_name, project=project, parent=None, created_by=developer)
        project.default_branch = default_branch
        project.save()
        WorksOn.objects.create(role="Owner", project=project, developer=developer)
        threading.Thread(target=self.gitea_create, args=([project, branch_name, username]), kwargs={}).start()
        return project
    
    def update(self, instance, validated_data):
        old_name = instance.name
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        branch_name = validated_data.get('default_branch_name', instance.default_branch.name)
        if branch_name != instance.default_branch.name:
            if Branch.objects.filter(name=branch_name, project=instance).exists():
                branch = Branch.objects.get(name=branch_name, project=instance)
                if branch:
                    instance.default_branch = branch
            else:
                raise Http404()
        instance.access_modifier = validated_data.get('access_modifier', instance.access_modifier)
        instance.save()
        owner_username = WorksOn.objects.get(project__name=instance.name, role='Owner').developer.user.username
        self.gitea_update(owner_username, instance, old_name)
        return instance

    def gitea_create(self, project, branch_name, username):
        description = ''
        if project.description is not None:
            description = project.description
        private = True
        if (project.access_modifier == "Public"):
            private = False
        gitea_service.create_repository({
            'default_branch': branch_name,
            'description': description,
            'name': project.name,
            'private': private
        }, username)

    def gitea_update(self, owner, repository, old_name):
        update_repository(owner, repository, old_name)
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class DeveloperSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Developer
        fields = ('user', 'gitea_token', 'avatar')