from rest_framework.permissions import BasePermission

from task_manager.constants.project import ProjectRole
from task_manager.models import ProjectMember


class IsProjectAdmin(BasePermission):
    message = 'You are not Project Admin'

    def has_object_permission(self, request, view, obj) -> bool:
        return ProjectMember.objects.filter(project=obj, member=request.user, role=ProjectRole.ADMIN).exists()

    def has_permission(self, request, view):
        project_key = view.kwargs.get('project_key')
        return ProjectMember.objects \
            .filter(project__key=project_key, member=request.user, role=ProjectRole.ADMIN) \
            .exists()
