from django.contrib.auth.models import User
from rest_framework import serializers
from main.gitea_service import *
from main.models import Developer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def update(self, instance, validated_data):
        old_username = instance.username
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        print(instance.username, old_username)
        self.gitea_update(instance.username, old_username)
        return instance

    def gitea_update(self, new_username, old_username):
        update_developer_username(new_username, old_username)


class DeveloperSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Developer
        fields = ('user', 'gitea_token', 'avatar')


