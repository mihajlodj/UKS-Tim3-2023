from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from main.models import Project, WorksOn

from repository.serializers import RepositorySerializer


class CreateRepositoryView(generics.CreateAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RepositorySerializer


class ReadRepositoryView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RepositorySerializer

    def get_object(self):
        owner_username = self.request.data.get('owner_username')
        repository_name = self.request.data.get('repository_name')
        works_on = WorksOn.objects.get(role='Owner', developer__user__username=owner_username, project__name=repository_name)
        return works_on.project
