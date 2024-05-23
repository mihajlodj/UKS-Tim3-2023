from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from main.models import Project, Milestone, Role, WorksOn
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
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER)
    if not works_on.exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    repository = works_on.first().project
    if not Milestone.objects.filter(title=title, project=repository).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    milestone = Milestone.objects.get(title=title, project=repository)
    gitea_service.delete_milestone_from_gitea(owner_username, repository.name, milestone.id_from_gitea)
    milestone.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository,])
def get_milestones_for_repo(request, owner_username, repository_name):
    works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name)
    milestones = Milestone.objects.filter(project=works_on.project)
    serialized_milestones = serialize_milestones(milestones)
    return Response(serialized_milestones, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository,])
def get_milestone(request, owner_username, repository_name, milestone_id):
    try:
        works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name)
        milestone = Milestone.objects.get(project=works_on.project, id=milestone_id)
        serialized_milestone = serialize_milestone(milestone)
        return Response(serialized_milestone, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        raise Http404()


def serialize_milestones(milestones):
    result = []
    for milestone in milestones:
        serialized_milestone = serialize_milestone(milestone)
        result.append(serialized_milestone)
    return result


def serialize_milestone(milestone):
    serialized_milestone = {
        'id': milestone.id,
        'title': milestone.title,
        'description': milestone.description,
        'state': milestone.state,
        'due_date': milestone.deadline,
        'labels': [],
    }
    for label in milestone.labels.all():
        serialized_milestone['labels'].append(serialize_label(label))
    return serialized_milestone


def serialize_label(label):
    return {
        'id': label.id,
        'name': label.name,
        'description': label.description
    }
