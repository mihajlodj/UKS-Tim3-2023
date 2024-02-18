from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from main.models import Label, Project, Milestone, Issue, PullRequest

from label.serializers import LabelSerializer

from main import permissions


class CreateLabelView(generics.CreateAPIView):
    queryset = Label.objects.all()
    permission_classes = (IsAuthenticated,permissions.CanEditRepository)
    serializer_class = LabelSerializer


class UpdateLabelView(generics.UpdateAPIView):
    queryset = Label.objects.all()
    permission_classes = (IsAuthenticated,permissions.CanUpdateLabel)
    serializer_class = LabelSerializer
    lookup_field = 'id'


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository])
def get_labels(request, repository_name):
    if not Project.objects.filter(name=repository_name).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    project = Project.objects.get(name=repository_name)
    labels = Label.objects.filter(project=project)
    serialized_labels = serialize_labels(labels)
    return Response(serialized_labels, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository])
def delete_label(request, label_id):
    if not label_id.isdigit():
        raise Http404()
    if not Label.objects.filter(id=label_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    label = Label.objects.get(id=label_id)
    label.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository])
def link_label_to_milestone(request, label_id, milestone_id):
    if not label_id.isdigit():
        raise Http404()
    if not Label.objects.filter(id=label_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not milestone_id.isdigit():
        raise Http404()
    if not Milestone.objects.filter(id=milestone_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    label = Label.objects.get(id=label_id)
    milestone = Milestone.objects.get(id=milestone_id)
    if label.project != milestone.project:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    milestone.labels.add(label)
    milestone.save()
    return Response(status=status.HTTP_200_OK)


def serialize_labels(labels):
    result = []
    for label in labels:
        result.append(serialize_label(label))
    return result


def serialize_label(label):
    return {
        'id': label.id,
        'name': label.name,
        'description': label.description
    }
