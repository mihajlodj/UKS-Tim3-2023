from main.models import WorksOn, AccessModifiers, Role, Project
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

class CanEditRepository(BasePermission):
    def has_object_permission(self, request, view, obj):
        logged_user = request.user.username
        if not WorksOn.objects.filter(project=obj, developer__user__username=logged_user).exists():
            return False
        role = WorksOn.objects.get(project=obj, developer__user__username=logged_user).role
        if role != Role.OWNER and role != Role.MAINTAINER:
            return False
        return True    

class CanCreateBranch(BasePermission):
    def has_permission(self, request, view):
        logged_user = request.user.username
        repository_name = view.kwargs.get('repository_name')
        works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repository_name)]
        if logged_user not in works_on_list:
            return False
        if WorksOn.objects.get(project__name=repository_name, developer__user__username=logged_user).role == Role.READONLY:
            return False
        return True
    
class CanViewRepository(BasePermission):
    def has_permission(self, request, view):
        repository_name = view.kwargs.get('repository_name')
        if not Project.objects.filter(name=repository_name).exists():
            return False
        repository = Project.objects.get(name=repository_name)
        if repository.access_modifier == AccessModifiers.PUBLIC:
            return True
        if not request.user.is_authenticated:
            return False
        logged_user = request.user.username
        works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repository.name)]
        return logged_user in works_on_list
    
class CanDeleteRepository(BasePermission):
    def has_permission(self, request, view):
        repository_name = view.kwargs.get('repository_name')
        if not Project.objects.filter(name=repository_name).exists():
            return False
        return WorksOn.objects.filter(developer__user__username=request.user.username, 
                                      project__name=repository_name, role=Role.OWNER).exists()
    
class CanEditRepositoryContent(BasePermission):
    def has_permission(self, request, view):
        repository_name = view.kwargs.get('repository_name')
        if not Project.objects.filter(name=repository_name).exists():
            return False
        logged_user = request.user.username
        works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repository_name)]
        if logged_user not in works_on_list:
            return False
        if WorksOn.objects.get(project__name=repository_name, developer__user__username=logged_user).role == Role.READONLY:
            return False
        return True

class CanUpdateMilestone(BasePermission):
    def has_object_permission(self, request, view, obj):
        repository_name = obj.project.name
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
    
class CanInviteCollaborator(BasePermission):
    def has_permission(self, request, view):
        repository_name = view.kwargs.get('repository_name')
        if not Project.objects.filter(name=repository_name).exists():
            return False
        works_on = WorksOn.objects.filter(developer__user__username=request.user.username, project__name=repository_name)
        if not works_on.exists():
            return False
        return works_on.first().role == Role.OWNER or works_on.first().role == Role.MAINTAINER

class CanTransferOwnership(BasePermission):
    def has_permission(self, request, view):
        repository_name = view.kwargs.get('repository_name')
        if not Project.objects.filter(name=repository_name).exists():
            return False
        return WorksOn.objects.filter(developer__user__username=request.user.username, 
                                      project__name=repository_name, role=Role.OWNER).exists()