from django.http import JsonResponse
from django.shortcuts import render
from git.refs import tag
from rest_framework.response import Response
from rest_framework import generics, status
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
import rest_framework.status as http_status

import main
from main import gitea_service, permissions
from main.models import Branch, Commit, Release, Tag, Project, WorksOn, Developer


# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_release(request, owner_username, project_name):
    release_title = request.data.get('title')
    release_description = request.data.get('description')
    branch_name = request.data.get('branch_name')
    release_pre_release = request.data.get('pre_release')
    release_draft = request.data.get('draft')
    tag_name = request.data.get('tag_name')
    caused_by_username = request.data.get('caused_by_username')

    worksOn = WorksOn.objects.get(project__name=project_name, developer__user__username=owner_username)
    repository = worksOn.project
    branch = Branch.objects.get(name=branch_name, project__name=project_name)
    commit = Commit.objects.filter(branch__id=branch.id, branch__project__id=repository.id).order_by('-timestamp')[0]

    try:
        Tag.objects.get(name=tag_name, project__id=repository.id)
        return JsonResponse({'message': 'Tag with this name already exists in the project'},
                            safe=False,
                            status=http_status.HTTP_409_CONFLICT)
    except main.models.Tag.DoesNotExist:
        dev = Developer.objects.get(user__username=caused_by_username)
        new_tag = Tag.objects.create(name=tag_name, project=repository, caused_by=dev)
        release = Release.objects.create(
            title=release_title,
            description=release_description,
            target=branch,
            pre_release=release_pre_release,
            draft=release_draft,
            tag=new_tag,
            commitish=commit.hash,
            project=repository
        )
        gitea_service.create_new_release(owner_username, repository_name=project_name, release=release)
        gitea_service.create_tag(owner_username, repository_name=project_name, tag=new_tag, branch_name=branch_name)

        release.save()
        # new_tag.save()
        commit.save()

        return JsonResponse(serialize_release(release), safe=False, status=http_status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_releases(request, owner_username, project_name):
    worksOn = WorksOn.objects.get(project__name=project_name, developer__user__username=owner_username)
    project = worksOn.project
    releases = Release.objects.filter(project__id=project.id)
    return JsonResponse([serialize_release(r) for r in releases], safe=False, status=200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_release(request, owner_username, project_name, tag_name):
    worksOn = WorksOn.objects.get(project__name=project_name, developer__user__username=owner_username)
    project = worksOn.project
    release = Release.objects.get(project__id=project.id, tag__name=tag_name)

    gitea_service.delete_release(owner_username, project_name, release)
    gitea_service.delete_tag(owner_username, project_name, tag_name)

    release.delete()  # CASCADE should delete tag object as well.
    return Response(data=None, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_release_by_tag_name(request, owner_username, project_name, tag_name):
    worksOn = WorksOn.objects.get(project__name=project_name, developer__user__username=owner_username)
    project = worksOn.project
    release = Release.objects.get(project__name=project_name, project__id=project.id, tag__name=tag_name)
    return JsonResponse(serialize_release(release), safe=False, status=http_status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_release_by_id(request, owner_username, project_name, release_id):
    release = Release.objects.get(id=release_id)
    return JsonResponse(serialize_release(release), safe=False, status=http_status.HTTP_200_OK)


def serialize_release(release):
    return {
        'title': release.title,
        'description': release.description,
        'branch': {
            'name': release.target.name,
            'id': release.target.id
        },
        'pre_release': release.pre_release,
        'draft': release.draft,
        'tag': serialize_tag(release.tag),
        'commitish': release.commitish,
        'project': release.project.name
    }


def serialize_tag(tag_obj):
    return {
        'id': tag_obj.id,
        'name': tag_obj.name
    }
