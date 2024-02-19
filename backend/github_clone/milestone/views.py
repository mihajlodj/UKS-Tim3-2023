from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from main.models import Project, Milestone, WorksOn
from milestone.serializers import MilestoneSerializer

from main.gitea_service import delete_milestone_from_gitea

from main import permissions, gitea_service


class CreateMilestoneView(generics.CreateAPIView):
    queryset = Milestone.objects.all()
    permission_classes = (IsAuthenticated,permissions.CanEditRepository,)
    serializer_class = MilestoneSerializer

class UpdateMilestoneView(generics.UpdateAPIView):
    queryset = Milestone.objects.all()
    permission_classes = (IsAuthenticated,permissions.CanUpdateMilestone,)
    serializer_class = MilestoneSerializer
    lookup_field = 'title'


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository])
def delete_milestone(request, owner_username, repository_name, title):
    if not Project.objects.filter(name=repository_name).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    repository = Project.objects.get(name=repository_name)
    if not Milestone.objects.filter(title=title, project=repository).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    milestone = Milestone.objects.get(title=title, project=repository)
    owner = WorksOn.objects.get(project__name=repository.name, role='Owner')
    gitea_service.delete_milestone_from_gitea(owner_username, repository.name, milestone.id_from_gitea)
    milestone.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository,])
def get_milestones_for_repo(request, repository_name):
    milestones = Milestone.objects.filter(project__name=repository_name)
    serialized_milestones = serialize_milestones(milestones)
    return Response(serialized_milestones, status=status.HTTP_200_OK)


def serialize_milestones(milestones):
    result = []
    for milestone in milestones:
        serialized_milestone = {
            'id': milestone.id,
            'title': milestone.title,
            'description': milestone.description,
            'state': milestone.state,
            'due_date': milestone.deadline,
        }
        result.append(serialized_milestone)
    return result
