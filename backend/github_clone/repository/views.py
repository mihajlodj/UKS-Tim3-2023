from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from main.models import Project, WorksOn, Developer, Branch
from rest_framework.decorators import api_view, permission_classes
from repository.serializers import RepositorySerializer, DeveloperSerializer
from main.gitea_service import get_root_content, get_repository, get_folder_content


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
        works_on = WorksOn.objects.get(role='Owner', developer__user__username=owner_username, project__name=repository_name)
        # TODO: permissions
        return works_on.project


class ReadOwnerView(generics.RetrieveAPIView):
    queryset = Developer.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = DeveloperSerializer

    def get_object(self):
        owner_username = self.kwargs.get('username')
        return Developer.objects.get(user__username=owner_username)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_repo_data_for_display(_, owner_username, repository_name):
    works_on = WorksOn.objects.get(role='Owner', developer__user__username=owner_username, project__name=repository_name)
    repo = works_on.project
    gitea_repo_data = get_repository(owner_username, repository_name)
    result = {'name': repo.name, 'description': repo.description, 'access_modifier': repo.access_modifier, 'default_branch': repo.default_branch.name, 
              'http': gitea_repo_data['clone_url'], 'ssh': gitea_repo_data['ssh_url'], 'branches': []}
    branches = Branch.objects.filter(project__name=repository_name)
    branches_names = [b.name for b in branches]
    result['branches'] = branches_names
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_root_files(_, owner_username, repository_name, ref):
    return Response(get_root_content(owner_username, repository_name, ref), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_folder_files(_, owner_username, repository_name, branch, path):
    return Response(get_folder_content(owner_username, repository_name, branch, path), status=status.HTTP_200_OK)