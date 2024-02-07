from main.models import WorksOn, AccessModifiers, Role
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


def can_view_repository(request, repository):
    logged_user = request.user.username
    if repository.access_modifier == AccessModifiers.PRIVATE:
        works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repository.name)]
        if logged_user not in works_on_list:
            raise PermissionDenied()
        
def can_delete_repository(request, repository):
    logged_user = request.user.username
    owner = WorksOn.objects.get(project__name=repository.name, role=Role.OWNER)
    if owner.developer.user.username != logged_user:
        raise PermissionDenied()
    
def can_edit_repository_content(request, repository):
    logged_user = request.user.username
    works_on_list = [obj.developer.user.username for obj in WorksOn.objects.filter(project__name=repository.name)]
    if logged_user not in works_on_list:
        raise PermissionDenied()
    if WorksOn.objects.get(project__name=repository.name, developer__user__username=logged_user).role == Role.READONLY:
        raise PermissionDenied()
    
