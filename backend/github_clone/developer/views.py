from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from developer.serializers import DeveloperSerializer, UserSerializer
from main.models import Developer
from main.gitea_service import get_gitea_user_info_gitea_service, get_gitea_user_emails_gitea_service


class UpdateDeveloperView(generics.UpdateAPIView):
    queryset = Developer.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = DeveloperSerializer
    lookup_field = 'user'


class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = 'username'


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_developers_avatar(request, username):
    user = User.objects.get(username=username)
    developer = Developer.objects.get(user_id=user.id)
    print(developer)
    developer.avatar = request.data.get('avatar')
    developer.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_info(request, username):
    user = User.objects.get(username=username)
    serializer_class = UserSerializer(user)
    print(serializer_class.data)
    return Response(serializer_class.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_gitea_user_info(request, username):
    gitea_user_info = get_gitea_user_info_gitea_service(username)
    return Response(gitea_user_info, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_developer_avatar(request, username):
    user = User.objects.get(username=username)
    developer = Developer.objects.get(user_id=user.id)
    return Response(developer.avatar, status=status.HTTP_200_OK)
    # gitea_user_info = get_gitea_user_info_gitea_service(username)
    # return Response(gitea_user_info['avatar_url'], status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_developers_emails(request, username):
    gitea_all_emails = get_gitea_user_emails_gitea_service()
    users_emails = [email for email in gitea_all_emails if username in email["username"]]
    return Response(users_emails, status=status.HTTP_200_OK)
