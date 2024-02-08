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
    if not Project.objects.filter(name=repository_name).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    repository = Project.objects.get(name=repository_name)
    if not Milestone.objects.filter(title=title, project=repository).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    milestone = Milestone.objects.get(title=title, project=repository)
    owner = WorksOn.objects.get(project__name=repository.name, role='Owner')
    check_delete_permission(request, repository, owner_username)
    delete_milestone_from_gitea(owner_username, repository.name, milestone.id_from_gitea)
    milestone.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_milestones_for_repo(request, repository_name):
    check_view_permission(request, repository_name)
    milestones = Milestone.objects.filter(project__name=repository_name)
    serialized_milestones = serialize_milestones(milestones)
    return Response(serialized_milestones, status=status.HTTP_200_OK)


def serialize_milestones(milestones):
    result = []
    for milestone in milestones:
        serialized_milestone = {
            'title': milestone.title,
            'description': milestone.description,
            'state': milestone.state,
            'due_date': milestone.deadline,
        }
        result.append(serialized_milestone)
    return result


def check_view_permission(request, repo_name):
    logged_user = request.user.username
    try:
        repo = Project.objects.get(name=repo_name)
        if repo.access_modifier == 'Private':
            works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repo.name)]
            if logged_user not in works_on_list:
                raise PermissionDenied()
    except ObjectDoesNotExist:
        raise Http404()


def check_delete_permission(request, repo, owner_username_arg):
    logged_user = request.user.username
    owner = WorksOn.objects.get(project__name=repo.name, role='Owner')
    if (owner.developer.user.username != logged_user) or (owner.developer.user.username != owner_username_arg):
        raise PermissionDenied()
