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
from rest_framework.permissions import IsAuthenticated, AllowAny

from developer import service
from developer.serializers import DeveloperSerializer, UserSerializer
from branch.serializers import BranchSerializer
from main import gitea_service
from main.models import Invitation, Role, WorksOn
from main.models import Developer, SecondaryEmail, Commit, Watches
from main.gitea_service import get_gitea_user_info_gitea_service
from main import permissions
from django.core.cache import cache
from datetime import datetime


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


@api_view(['GET'])
def get_all_devs(request, query):
    repositories = None

    parts = query.split('&')
    for part in parts:
        if 'repositories:' in part:
            repositories = int(part.split('repositories:', 1)[1].strip())
        else:
            query = part.strip()

    cache_key = f"developer_query:{query}{repositories}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    all_results = Developer.objects.all()
    results = []
    for result in all_results:
        if result.user.username.lower().__contains__(query.lower()):
            results.append(result)

    if len(results) > 0:
        serialized_data = []
        for result in results:
            isExcluded = False
            developer_serializer = DeveloperSerializer(result)
            developer = developer_serializer.data
            print(developer)

            if repositories is not None:
                allUserRepos = len(Watches.objects.filter(developer__user__username__contains=developer['user']['username'],developer__workson__role__exact="Owner"))
                if allUserRepos < repositories:
                    isExcluded = True
            if not isExcluded:
                serialized_data.append(developer)

        cache.set(cache_key, serialized_data, timeout=30)

        return Response(serialized_data, status=status.HTTP_200_OK)
    else:
        return Response([], status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_commits(request, query):
    owner = ''
    committer = ''
    created_date = None

    parts = query.split('&')
    for part in parts:
        if 'owner:' in part:
            owner = part.split('owner:', 1)[1].strip()
        elif 'committer:' in part:
            committer = part.split('committer:', 1)[1].strip()
        elif 'created:' in part:
            created_date = datetime.strptime(part.split('created:', 1)[1].strip(), '%d-%m-%Y').date()
        else:
            query = part.strip()



    cache_key = f"commit_query:{query}{owner}{committer}{created_date}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    # results = Commit.objects.filter(message__contains=query)
    results = Commit.objects.all()

    if query:
        results = results.filter(message__contains=query)
    if owner:
        results = results.filter(author__user__username__contains=owner)
    if committer:
        results = results.filter(committer__user__username__contains=committer)
    if created_date:
        results = results.filter(timestamp__gt=created_date)

    if results.exists():
        serialized_data = []
        for result in results:
            author_serializer = DeveloperSerializer(result.author)
            author = author_serializer.data

            committer_serializer = DeveloperSerializer(result.committer)
            committer = committer_serializer.data

            branch_serializer = BranchSerializer(result.branch)
            branch = branch_serializer.data

            serialized_data.append(
                {'message': result.message, 'branch': branch, 'author': author,
                 'committer': committer, 'timestamp': result.timestamp})

        cache.set(cache_key, serialized_data, timeout=30)

        return Response(serialized_data, status=status.HTTP_200_OK)
    else:
        return Response([], status=status.HTTP_200_OK)


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
                response_gitea = gitea_service.change_gitea_user_password_gitea_service(username, new_password)
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
    # if developer.avatar is not None:
    #     os.remove(developer.avatar[7:])
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
@permission_classes([AllowAny])
def get_developer_avatar(request, username):
    return Response(service.get_dev_avatar(username), status=status.HTTP_200_OK)


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


@api_view(['GET'])
def get_developers(request, owner_username, repository_name):
    developers = Developer.objects.filter()
    project = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).project
    result = [{
        'username': d.user.username,
        'avatar': service.get_dev_avatar(d.user.username),
        'email': d.user.email
        } for d in developers
        if not WorksOn.objects.filter(developer=d, project=project).exists()
            and not Invitation.objects.filter(developer=d, project=project).exists()]
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_developer_roles(request, username):
    works_on_list = WorksOn.objects.filter(developer__user__username=username)
    result = [{
        'repository': obj.project.name,
        'role': obj.role
    } for obj in works_on_list]
    return Response(result, status=status.HTTP_200_OK)
