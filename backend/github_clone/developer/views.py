import os

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files import File
from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from developer.serializers import DeveloperSerializer, UserSerializer
from main.models import Developer, SecondaryEmail
from main.gitea_service import get_gitea_user_info_gitea_service, get_gitea_user_emails_gitea_service, \
    change_gitea_user_password_gitea_service, delete_gitea_user_gitea_service


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_new_email(request, username):
    user = User.objects.get(username=username)
    developer = Developer.objects.get(user_id=user.id)
    print(request.data.get('secondary_emails'))
    secondary_email = SecondaryEmail.objects.create(
        developer=developer,
        email=request.data.get('secondary_emails')
    )
    secondary_email.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_users_password(request, username):
    try:
        user = User.objects.get(username=username)
        print(user.check_password(request.data.get('current_password')))
        if user.check_password(request.data.get('current_password')):
            new_password = request.data.get('new_password')
            new_password_repeat = request.data.get('new_password_repeat')
            if new_password == new_password_repeat:
                user.set_password(new_password)
                user.save()
                print(new_password)
                response_gitea = change_gitea_user_password_gitea_service(username, new_password)
                print(response_gitea)
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_developer(request, usersPassowrd, username):
    user = User.objects.get(username=username)
    developer = Developer.objects.get(user_id=user.id)
    if user.check_password(usersPassowrd):
        developer.delete()
        user.delete()
        # response_gitea = delete_gitea_user_gitea_service(username)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_developers_avatar(request, username):
    user = User.objects.get(username=username)
    developer = Developer.objects.get(user_id=user.id)
    if developer.avatar is not None:
        os.remove(developer.avatar)
    developer.avatar = None
    developer.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_developers_email(request, username, usersEmail):
    email_to_delete = SecondaryEmail.objects.get(email=usersEmail)
    email_to_delete.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_developers_avatar(request, username):
    user = User.objects.get(username=username)
    developer = Developer.objects.get(user_id=user.id)

    if developer.avatar is not None:
        os.remove(developer.avatar)

    if 'avatar' in request.FILES:
        avatar = request.FILES['avatar']

        avatars_directory = os.path.join('avatars')
        os.makedirs(avatars_directory, exist_ok=True)

        avatar_path = os.path.join(avatars_directory, avatar.name)

        with open(avatar_path, 'wb') as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)

        developer.avatar = avatar_path
        developer.save()

        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


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

    if developer.avatar is None:
        gitea_user_info = get_gitea_user_info_gitea_service(username)
        return Response(gitea_user_info['avatar_url'], status=status.HTTP_200_OK)

    avatar_filename = developer.avatar
    avatar_filename = avatar_filename.split('/')[3]
    avatar_url = f"http://localhost/avatars/{avatar_filename}"
    return Response(avatar_url, status=status.HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_developers_emails_gitea(request, username):
#     gitea_all_emails = get_gitea_user_emails_gitea_service()
#     users_emails = [email for email in gitea_all_emails if username in email["username"]]
#     return Response(users_emails, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_developers_emails(request, username):
    user = User.objects.get(username=username)
    developer = Developer.objects.get(user_id=user.id)
    emails = SecondaryEmail.objects.filter(developer_id=developer.id)
    users_emails = [{'email': email.email, 'primary': email.primary, 'verified': email.verified} for email in emails]
    primary_email = user.email
    users_emails.append({'email': primary_email, 'primary': True, 'verified': True})
    return Response(users_emails[::-1], status=status.HTTP_200_OK)
