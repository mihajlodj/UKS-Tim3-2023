from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from main.models import Project, Milestone, Role, WorksOn, MilestoneState, EventHistory
from milestone.serializers import MilestoneSerializer
import threading
from websocket import notification_service
from main.gitea_service import delete_milestone_from_gitea

from main import permissions, gitea_service


class CreateMilestoneView(generics.CreateAPIView):
    queryset = Milestone.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MilestoneSerializer

class UpdateMilestoneView(generics.UpdateAPIView):
    queryset = Milestone.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MilestoneSerializer
    lookup_field = 'title'


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_milestone(request, owner_username, repository_name, title):
    works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name, role='Owner')
    repository = works_on.project
    if not Milestone.objects.filter(title=title, project=repository).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    project = works_on.project
    owner = works_on.developer
    milestone = Milestone.objects.get(title=title, project=repository)
    gitea_service.delete_milestone_from_gitea(owner_username, repository.name, milestone.id_from_gitea)
    milestone.delete()
    milestone_info = {
        'creator': request.user.username,
        'title': milestone.title,
    }
    threading.Thread(target=notification_service.send_notification_milestone_deleted,
                     args=([owner.user.username, project, milestone_info]), kwargs={}).start()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_milestones_for_repo(request, owner_username, repository_name):
    works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name)
    milestones = Milestone.objects.filter(project=works_on.project)
    serialized_milestones = serialize_milestones(milestones)
    return Response(serialized_milestones, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_milestone(request, owner_username, repository_name, milestone_id):
    try:
        works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name)
        milestone = Milestone.objects.get(project=works_on.project, id=milestone_id)
        serialized_milestone = serialize_milestone(milestone)
        return Response(serialized_milestone, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        raise Http404()


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def close_milestone(request, owner_username, repository_name, milestone_id):
    try:
        works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name)
        milestone = Milestone.objects.get(project=works_on.project, id=milestone_id)
        if milestone.state != MilestoneState.OPEN:
            return HttpResponse(status=400)
        milestone.state = MilestoneState.CLOSED
        milestone.save()
        project = works_on.project
        owner = works_on.developer
        milestone_info = {
            'creator': request.user.username,
            'title': milestone.title,
        }
        threading.Thread(target=notification_service.send_notification_milestone_closed,
                         args=([owner.user.username, project, milestone_info]), kwargs={}).start()
        EventHistory.objects.create(project=milestone.project, related_id=milestone.id,
                                    text=f"{request.user.username} closed milestone")
        return HttpResponse(status=200)
    except ObjectDoesNotExist:
        raise Http404()


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def reopen_milestone(request, owner_username, repository_name, milestone_id):
    try:
        works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name)
        milestone = Milestone.objects.get(project=works_on.project, id=milestone_id)
        if milestone.state != MilestoneState.CLOSED:
            return HttpResponse(status=400)
        milestone.state = MilestoneState.OPEN
        milestone.save()
        project = works_on.project
        owner = works_on.developer
        milestone_info = {
            'creator': request.user.username,
            'title': milestone.title,
        }
        threading.Thread(target=notification_service.send_notification_milestone_reopened,
                         args=([owner.user.username, project, milestone_info]), kwargs={}).start()
        EventHistory.objects.create(project=milestone.project, related_id=milestone.id,
                                    text=f"{request.user.username} reopened milestone")
        return HttpResponse(status=200)
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
