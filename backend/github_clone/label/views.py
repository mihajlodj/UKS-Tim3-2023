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
def get_labels(request, owner_username, repository_name):
    if not Project.objects.filter(name=repository_name).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    project = Project.objects.get(name=repository_name)
    labels = Label.objects.filter(project=project)
    serialized_labels = serialize_labels(labels)
    return Response(serialized_labels, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository])
def delete_label(request, owner_username, repository_name, label_id):
    if not label_id.isdigit():
        raise Http404()
    if not Label.objects.filter(id=label_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    label = Label.objects.get(id=label_id)
    label.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository])
def link_label_to_milestone(request, owner_username, repository_name, label_id, milestone_id):
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


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository])
def link_label_to_issue(request, owner_username, repository_name, label_id, issue_id):
    if not label_id.isdigit():
        raise Http404()
    if not Label.objects.filter(id=label_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not issue_id.isdigit():
        raise Http404()
    if not Issue.objects.filter(id=issue_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    label = Label.objects.get(id=label_id)
    issue = Issue.objects.get(id=issue_id)
    if label.project != issue.project:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    issue.labels.add(label)
    issue.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository])
def link_label_to_pull_request(request, owner_username, repository_name, label_id, pull_request_id):
    if not label_id.isdigit():
        raise Http404()
    if not Label.objects.filter(id=label_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not pull_request_id.isdigit():
        raise Http404()
    if not Issue.objects.filter(id=pull_request_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    label = Label.objects.get(id=label_id)
    pull_request = PullRequest.objects.get(id=pull_request_id)
    if label.project != pull_request.project:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    pull_request.labels.add(label)
    pull_request.save()
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
