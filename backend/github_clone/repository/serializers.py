import threading
from rest_framework import serializers
from django.core.validators import RegexValidator

from main import gitea_service
from main.models import Project, AccessModifiers, Branch, Role, WorksOn, Developer, Watches, WatchOption
from django.contrib.auth.models import User


class RepositorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=255, 
                                 validators=[RegexValidator(regex=r'^[a-zA-Z][\w-]*$', message="Invalid repository name", code="invalid_repo_name")])
    description = serializers.CharField(required=False, allow_blank=True)
    access_modifier = serializers.ChoiceField(choices=AccessModifiers, default='Public')
    default_branch_name = serializers.CharField(required=False, allow_blank=True, max_length=255,
                                                validators=[RegexValidator(regex=r'^[a-zA-Z][\w-]*$', message="Invalid branch name", code="invalid_branch_name")])

    def validate_name(self, value):
        username = self.context['request'].auth.get('username', None)
        repos = Project.objects.filter(name=value)
        for repo in repos:
            if WorksOn.objects.filter(developer__user__username=username, project=repo, role=Role.OWNER).exists():
                raise serializers.ValidationError("Repository with this name already exists for this owner.")
        return value

    
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
        Watches.objects.create(developer=developer, project=project, option=WatchOption.ALL)
        threading.Thread(target=self.gitea_create, args=([project, branch_name, username]), kwargs={}).start()
        return project
    

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
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class DeveloperSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Developer
        fields = ('user', 'gitea_token', 'avatar')