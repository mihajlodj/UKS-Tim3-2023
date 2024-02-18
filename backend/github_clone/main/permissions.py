import os

from django.http import Http404

from main.models import WorksOn, AccessModifiers, Role, Developer
from rest_framework.permissions import BasePermission

GITEA_ADMIN_USERNAME = os.environ.get("GITEA_ADMIN_USERNAME")

class CanEditRepository(BasePermission):
    def has_permission(self, request, view):
        logged_user = request.user.username
        developer = Developer.objects.get(user__username=logged_user)
        repository_name = view.kwargs.get('repository_name')
        owner_username = view.kwargs.get('owner_username')
        if developer.banned:
            return False

        if logged_user == GITEA_ADMIN_USERNAME:
            return True
        
        works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER)
        if not works_on.exists():
            raise Http404()
        project = works_on.first().project

        if not WorksOn.objects.filter(project=project, developer__user__username=logged_user).exists():
            return False
        role = WorksOn.objects.get(project=project, developer__user__username=logged_user).role
        if role != Role.OWNER and role != Role.MAINTAINER:
            return False
        return True


class CanCreateBranch(BasePermission):
    def has_permission(self, request, view):
        logged_user = request.user.username
        developer = Developer.objects.get(user__username=logged_user)
        if developer.banned:
            return False
        if logged_user == GITEA_ADMIN_USERNAME:
            return True
        repository_name = view.kwargs.get('repository_name')
        works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repository_name)]
        if logged_user not in works_on_list:
            return False
        role = WorksOn.objects.get(project__name=repository_name, developer__user__username=logged_user).role
        return role != Role.READONLY and role != Role.IS_BANNED


class CanViewRepository(BasePermission):
    def has_permission(self, request, view):
        repository_name = view.kwargs.get('repository_name')
        owner_username = view.kwargs.get('owner_username')
        if not WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                      role=Role.OWNER).exists():
            return False
        works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name,
                                       role=Role.OWNER)
        repository = works_on.project
        if repository.access_modifier == AccessModifiers.PUBLIC:
            return True
        logged_user = request.user.username
        if logged_user == GITEA_ADMIN_USERNAME:
            return True
        if not request.user.is_authenticated:
            return False
        works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repository.name)]
        return logged_user in works_on_list


class CanDeleteRepository(BasePermission):
    def has_permission(self, request, view):
        repository_name = view.kwargs.get('repository_name')
        owner_username = view.kwargs.get('owner_username')
        if not WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                      role=Role.OWNER).exists():
            return False
        logged_user = request.user.username
        developer = Developer.objects.get(user__username=logged_user)
        if developer.banned:
            return False
        if logged_user == GITEA_ADMIN_USERNAME:
            return WorksOn.objects.filter(project__name=repository_name).exists()
        return WorksOn.objects.filter(developer__user__username=logged_user, project__name=repository_name,
                                      role=Role.OWNER).exists()


class CanEditRepositoryContent(BasePermission):
    def has_permission(self, request, view):
        repository_name = view.kwargs.get('repository_name')
        owner_username = view.kwargs.get('owner_username')
        if not WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                      role=Role.OWNER).exists():
            return False
        logged_user = request.user.username
        developer = Developer.objects.get(user__username=logged_user)
        if developer.banned:
            return False
        if logged_user == GITEA_ADMIN_USERNAME:
            return True
        works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repository_name)]
        if logged_user not in works_on_list:
            return False
        role = WorksOn.objects.get(project__name=repository_name, developer__user__username=logged_user).role
        return role != Role.READONLY and role != Role.IS_BANNED


class CanUpdateMilestone(BasePermission):
    def has_object_permission(self, request, view, obj):
        repository_name = obj.project.name
        owner_username = view.kwargs.get('owner_username')
        if not WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                      role=Role.OWNER).exists():
            return False
        works_on = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name,
                                       role=Role.OWNER)
        project = works_on.project
        logged_user = request.user.username
        developer = Developer.objects.get(user__username=logged_user)
        if developer.banned:
            return False
        if logged_user == GITEA_ADMIN_USERNAME:
            return True
        if not WorksOn.objects.filter(project=project, developer__user__username=logged_user).exists():
            return False
        role = WorksOn.objects.get(project=project, developer__user__username=logged_user).role
        if role != Role.OWNER and role != Role.MAINTAINER:
            return False
        return True


class CanInviteCollaborator(BasePermission):
    def has_permission(self, request, view):
        repository_name = view.kwargs.get('repository_name')
        owner_username = view.kwargs.get('owner_username')
        if not WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                      role=Role.OWNER).exists():
            return False
        works_on = WorksOn.objects.filter(developer__user__username=request.user.username,
                                          project__name=repository_name)
        if not works_on.exists():
            return False
        logged_user = request.user.username
        developer = Developer.objects.get(user__username=logged_user)
        if developer.banned:
            return False
        if logged_user == GITEA_ADMIN_USERNAME:
            return WorksOn.objects.filter(project__name=repository_name).exists()
        return works_on.first().role == Role.OWNER or works_on.first().role == Role.MAINTAINER


class CanTransferOwnership(BasePermission):
    def has_permission(self, request, view):
        logged_user = request.user.username
        developer = Developer.objects.get(user__username=logged_user)
        if developer.banned:
            return False
        repository_name = view.kwargs.get('repository_name')
        owner_username = view.kwargs.get('owner_username')
        if not WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name,
                                      role=Role.OWNER).exists():
            return False
        return WorksOn.objects.filter(developer__user__username=request.user.username, project__name=repository_name,
                                      role=Role.OWNER).exists()

class CanUpdateLabel(BasePermission):
    def has_object_permission(self, request, view, obj):
        repository_name = obj.project.name
        print(repository_name)
        if not Project.objects.filter(name=repository_name).exists():
            return False
        project = Project.objects.get(name=repository_name)
        logged_user = request.user.username
        if not WorksOn.objects.filter(project=project, developer__user__username=logged_user).exists():
            return False
        role = WorksOn.objects.get(project=project, developer__user__username=logged_user).role
        if role != Role.OWNER and role != Role.MAINTAINER:
            return False
        return True
