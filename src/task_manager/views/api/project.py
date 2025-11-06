from django.db.models import Subquery
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from task_manager.constants.project import ProjectRole
from task_manager.models import Project, ProjectMember
from task_manager.permissions.project import IsProjectAdmin
from task_manager.serializers.project import ProjectDetailSerializer, ProjectNewMemberSerializer, ProjectSerializer


@extend_schema(tags=['Project'])
class ProjectViewSet(viewsets.ModelViewSet):
    lookup_field = 'key'
    lookup_url_kwarg = 'project_key'

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


@extend_schema(
    tags=['Project'],
    request=ProjectNewMemberSerializer,
    responses={status.HTTP_200_OK: ProjectDetailSerializer}
)
class ProjectMemberView(generics.CreateAPIView):
    permission_classes = [IsProjectAdmin]

    def create(self, request, *args, **kwargs):
        project_key = kwargs.get('project_key')
        project = get_object_or_404(Project, key=project_key)

        serializer = self.get_serializer(data=request.data, instance=project)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(ProjectDetailSerializer(project).data)
