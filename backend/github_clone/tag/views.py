from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from main import gitea_service
from main.models import Tag, WorksOn, Commit


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tags(request, owner_username, project_name):
    worksOn = WorksOn.objects.get(project__name=project_name, developer__user__username=owner_username)
    project = worksOn.project
    tags = Tag.objects.filter(project__id=project.id)
    return_data = []
    for t in tags:
        commits = Commit.objects.filter(tags__id=t.id)
        for c in commits:
            return_data.append(serialize_tag(t, c))
    return JsonResponse(return_data, safe=False, status=200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tag(request, owner_username, project_name, tag_id):
    tag_id = int(tag_id)
    tag = Tag.objects.get(id=tag_id)
    gitea_service.delete_tag(owner_username=owner_username, repository_name=project_name, tag_name=tag.name)
    tag.delete()
    return Response(status=200)


def serialize_tag(tag_obj, commit):
    return {
        'id': tag_obj.id,
        'name': tag_obj.name,
        'commit': serialize_commit(commit),
        'caused_by': tag_obj.caused_by.user.username
    }


def serialize_commit(commit):
    return {
        'hash': str(commit.hash),
        'message': commit.message,
        'timestamp': commit.timestamp
    }

