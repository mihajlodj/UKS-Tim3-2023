from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from main.models import Project, AccessModifiers, Branch


class RepositorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=255, 
                                 validators=[UniqueValidator(queryset=Project.objects.all())])
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
        return project
    