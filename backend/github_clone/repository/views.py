from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from main.models import Project, WorksOn, Developer

from repository.serializers import RepositorySerializer, DeveloperSerializer


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
