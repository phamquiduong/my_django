from django.db.models import Subquery
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from task_manager.constants.project import ProjectRole
from task_manager.models import Project, ProjectMember
from task_manager.permissions.project import IsProjectAdmin
from task_manager.serializers.project import ProjectDetailSerializer, ProjectSerializer


@extend_schema(tags=['Projects'])
class ProjectViewSet(viewsets.ModelViewSet):
    lookup_field = 'key'

    def perform_create(self, serializer) -> None:
        project = serializer.save()
        ProjectMember.objects.create(project=project, member=self.request.user, role=ProjectRole.ADMIN)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer

    def get_queryset(self):
        projects_of_auth_user = ProjectMember.objects.filter(member=self.request.user).values('project')
        return Project.objects.filter(id__in=Subquery(projects_of_auth_user))

    def get_permissions(self):
        permission_classes: list = [IsAuthenticated()]
        if self.request.method not in SAFE_METHODS:
            permission_classes.append(IsProjectAdmin())
        return permission_classes
