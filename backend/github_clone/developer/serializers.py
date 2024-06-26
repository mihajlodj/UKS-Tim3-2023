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
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        self.gitea_update(instance.username, old_username,
                          instance.first_name, instance.last_name)
        return instance

    def gitea_update(self, new_username, old_username,new_first_name,new_last_name):
        update_developer_username(new_username, old_username)
        update_developer_info(new_username,new_first_name,new_last_name)


class DeveloperSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Developer
        fields = ('user','gitea_token', 'avatar','banned')

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance
