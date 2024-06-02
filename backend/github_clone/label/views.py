from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
import threading
from websocket import notification_service

from main.models import Label, Project, Milestone, Issue, PullRequest, PullRequestReviewer, WorksOn, EventHistory

from label.serializers import LabelSerializer

from main import permissions


class CreateLabelView(generics.CreateAPIView):
    queryset = Label.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LabelSerializer


class UpdateLabelView(generics.UpdateAPIView):
    queryset = Label.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LabelSerializer
    lookup_field = 'id'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_labels(request, owner_username, repository_name):
    if not Project.objects.filter(name=repository_name).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    project = Project.objects.get(name=repository_name)
    labels = Label.objects.filter(project=project)
    serialized_labels = serialize_labels(labels)
    return Response(serialized_labels, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_label(request, owner_username, repository_name, label_id):
    project_name = request.parser_context.get('kwargs').get('repository_name', None)
    owner_username = request.parser_context.get('kwargs').get('owner_username', None)
    label_creator = request.user.username

    works_on = WorksOn.objects.get(role='Owner', project__name=project_name, developer__user__username=owner_username)
    owner = works_on.developer
    project = Project.objects.get(name=project_name)

    if not label_id.isdigit():
        raise Http404()
    if not Label.objects.filter(id=label_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    label = Label.objects.get(id=label_id)
    label.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def link_label_to_milestone(request, owner_username, repository_name, label_id, milestone_id):
    project_name = request.parser_context.get('kwargs').get('repository_name', None)
    owner_username = request.parser_context.get('kwargs').get('owner_username', None)
    label_creator = request.user.username

    works_on = WorksOn.objects.get(role='Owner', project__name=project_name, developer__user__username=owner_username)
    owner = works_on.developer
    project = Project.objects.get(name=project_name)

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
    EventHistory.objects.create(project=milestone.project, related_id=milestone.id,
                                text=f"{request.user.username} added label {label.name} to milestone")
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def unlink_label_to_milestone(request, owner_username, repository_name, label_id, milestone_id):
    project_name = request.parser_context.get('kwargs').get('repository_name', None)
    owner_username = request.parser_context.get('kwargs').get('owner_username', None)
    label_creator = request.user.username

    works_on = WorksOn.objects.get(role='Owner', project__name=project_name, developer__user__username=owner_username)
    owner = works_on.developer
    project = Project.objects.get(name=project_name)

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
    milestone.labels.remove(label)
    milestone.save()
    EventHistory.objects.create(project=milestone.project, related_id=milestone.id,
                                text=f"{request.user.username} removed label {label.name} from milestone")
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def link_label_to_issue(request, owner_username, repository_name, label_id, issue_id):
    project_name = request.parser_context.get('kwargs').get('repository_name', None)
    owner_username = request.parser_context.get('kwargs').get('owner_username', None)
    label_creator = request.user.username

    works_on = WorksOn.objects.get(role='Owner', project__name=project_name, developer__user__username=owner_username)
    owner = works_on.developer
    project = Project.objects.get(name=project_name)

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
    EventHistory.objects.create(project=issue.project, related_id=issue.id,
                                text=f"{request.user.username} added label {label.name} to issue")
    label_info = {
        'creator': label_creator,
        'label_name': label.name,
        'joined_entity_name': issue.title,
        'issue_creator': issue.creator.user.username
    }
    threading.Thread(target=notification_service.send_notification_label_added_on_issue,
                     args=([owner.user.username, project, label_info]), kwargs={}).start()
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def unlink_label_to_issue(request, owner_username, repository_name, label_id, issue_id):
    project_name = request.parser_context.get('kwargs').get('repository_name', None)
    owner_username = request.parser_context.get('kwargs').get('owner_username', None)
    label_creator = request.user.username

    works_on = WorksOn.objects.get(role='Owner', project__name=project_name, developer__user__username=owner_username)
    owner = works_on.developer
    project = Project.objects.get(name=project_name)

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
    issue.labels.remove(label)
    issue.save()

    label_info = {
        'creator': label_creator,
        'label_name': label.name,
        'joined_entity_name': issue.title,
        'issue_creator': issue.creator.user.username
    }
    threading.Thread(target=notification_service.send_notification_label_removed_from_issue,
                     args=([owner.user.username, project, label_info]), kwargs={}).start()
    EventHistory.objects.create(project=issue.project, related_id=issue.id,
                                text=f"{request.user.username} removed label {label.name} from issue")
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def link_label_to_pull_request(request, owner_username, repository_name, label_id, pull_request_id):
    project_name = request.parser_context.get('kwargs').get('repository_name', None)
    owner_username = request.parser_context.get('kwargs').get('owner_username', None)
    label_creator = request.user.username

    works_on = WorksOn.objects.get(role='Owner', project__name=project_name, developer__user__username=owner_username)
    owner = works_on.developer
    project = works_on.project

    if not label_id.isdigit():
        raise Http404()
    if not Label.objects.filter(id=label_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not pull_request_id.isdigit():
        raise Http404()
    if not PullRequest.objects.filter(project=project, gitea_id=pull_request_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    label = Label.objects.get(id=label_id)
    pull_request = PullRequest.objects.get(project=project, gitea_id=pull_request_id)
    if label.project != pull_request.project:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    pull_request.labels.add(label)
    pull_request.save()

    pull_request_reviewers = []
    for object in PullRequestReviewer.objects.filter(pull_request=pull_request):
        pull_request_reviewers.append(object.reviewer.user.username)
    pull_request_assignee = ''
    if pull_request.assignee is not None:
        pull_request_assignee = pull_request.assignee.user.username

    label_info = {
        'creator': label_creator,
        'label_name': label.name,
        'joined_entity_name': pull_request.title,
        'pr_assignee': pull_request_assignee,
        'pr_reviewers': pull_request_reviewers,
        'pr_author': pull_request.author.user.username
    }
    threading.Thread(target=notification_service.send_notification_label_added_on_pull_request,
                     args=([owner.user.username, project, label_info]), kwargs={}).start()
    EventHistory.objects.create(project=pull_request.project, related_id=pull_request.gitea_id,
                                text=f"{request.user.username} added label {label.name} to pull request")
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def unlink_label_to_pull_request(request, owner_username, repository_name, label_id, pull_request_id):
    project_name = request.parser_context.get('kwargs').get('repository_name', None)
    owner_username = request.parser_context.get('kwargs').get('owner_username', None)
    label_creator = request.user.username

    works_on = WorksOn.objects.get(role='Owner', project__name=project_name, developer__user__username=owner_username)
    owner = works_on.developer
    project = works_on.project

    if not label_id.isdigit():
        raise Http404()
    if not Label.objects.filter(id=label_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not pull_request_id.isdigit():
        raise Http404()
    if not PullRequest.objects.filter(project=project, gitea_id=pull_request_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    label = Label.objects.get(id=label_id)
    pull_request = PullRequest.objects.get(project=project, gitea_id=pull_request_id)
    if label.project != pull_request.project:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    pull_request.labels.remove(label)
    pull_request.save()

    pull_request_reviewers = []
    for object in PullRequestReviewer.objects.filter(pull_request=pull_request):
        pull_request_reviewers.append(object.reviewer.user.username)
    pull_request_assignee = ''
    if pull_request.assignee is not None:
        pull_request_assignee = pull_request.assignee.user.username

    label_info = {
        'creator': label_creator,
        'label_name': label.name,
        'joined_entity_name': pull_request.title,
        'pr_assignee': pull_request_assignee,
        'pr_reviewers': pull_request_reviewers,
        'pr_author': pull_request.author.user.username 
    }
    threading.Thread(target=notification_service.send_notification_label_removed_from_pull_request,
                     args=([owner.user.username, project, label_info]), kwargs={}).start()
    EventHistory.objects.create(project=pull_request.project, related_id=pull_request.gitea_id,
                                text=f"{request.user.username} removed label {label.name} from pull request")
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
