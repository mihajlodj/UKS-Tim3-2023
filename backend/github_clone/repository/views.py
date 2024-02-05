from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from main.models import Project, WorksOn, Developer, Branch, AccessModifiers
from rest_framework.decorators import api_view, permission_classes
from repository.serializers import RepositorySerializer, DeveloperSerializer
from main.gitea_service import get_root_content, get_repository, get_folder_content, delete_repository
from rest_framework.exceptions import PermissionDenied


class CreateRepositoryView(generics.CreateAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RepositorySerializer

class ReadRepositoryView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RepositorySerializer

    def get_object(self):
        owner_username = self.kwargs.get('owner_username')
        repository_name = self.kwargs.get('repository_name')
        works_on = WorksOn.objects.get(role='Owner', developer__user__username=owner_username,
                                       project__name=repository_name)
        # TODO: permissions
        logged_user = self.context['request'].auth.get('username', None)
        print(logged_user)
        return works_on.project


class ReadOwnerView(generics.RetrieveAPIView):
    queryset = Developer.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = DeveloperSerializer

    def get_object(self):
        owner_username = self.kwargs.get('username')
        return Developer.objects.get(user__username=owner_username)


class UpdateRepositoryView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RepositorySerializer
    lookup_field = 'name'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_repo_data_for_display(request, owner_username, repository_name):
    repo = Project.objects.get(name=repository_name)
    check_view_permission(request, repo)
    gitea_repo_data = get_repository(owner_username, repository_name)
    result = {'name': repo.name, 'description': repo.description, 'access_modifier': repo.access_modifier,
              'default_branch': repo.default_branch.name,
              'http': gitea_repo_data['clone_url'], 'ssh': gitea_repo_data['ssh_url'], 'branches': []}
    branches = Branch.objects.filter(project__name=repository_name)
    branches_names = [b.name for b in branches]
    result['branches'] = branches_names
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_root_files(request, owner_username, repository_name, ref):
    check_view_permission(request, Project.objects.get(name=repository_name))
    return Response(get_root_content(owner_username, repository_name, ref), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_folder_files(request, owner_username, repository_name, branch, path):
    check_view_permission(request, Project.objects.get(name=repository_name))
    return Response(get_folder_content(owner_username, repository_name, branch, path), status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_repo(request, owner_username, repository_name):
    if not Project.objects.filter(name=repository_name).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    repository = Project.objects.get(name=repository_name)
    check_delete_permission(request, repository)
    works_on_list = WorksOn.objects.filter(project__name=repository_name)
    for item in works_on_list:
        item.delete()
    delete_repository(owner_username, repository_name)
    repository.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users_repo(request, owner_username):
    user = User.objects.get(username=owner_username)
    developer = Developer.objects.get(user_id=user.id)
    repos = []
    for temp_repo in WorksOn.objects.filter(developer_id=developer.id):
        repo = Project.objects.get(id=temp_repo.project_id)
        isPrivate = False
        if repo.access_modifier == AccessModifiers.PRIVATE:
            isPrivate = True
        result = {'name': repo.name, 'description': repo.description, 'access_modifier': isPrivate,
                  'default_branch': repo.default_branch.name}
        repos.append(result)
    return Response(repos, status=status.HTTP_200_OK)


def check_view_permission(request, repo):
    logged_user = request.user.username
    if repo.access_modifier == 'Private':
        works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repo.name)]
        if logged_user not in works_on_list:
            raise PermissionDenied()


def check_delete_permission(request, repo):
    logged_user = request.user.username
    owner = WorksOn.objects.get(project__name=repo.name, role='Owner')
    if owner.developer.user.username != logged_user:
        raise PermissionDenied()
