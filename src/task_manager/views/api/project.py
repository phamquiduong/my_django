from django.contrib.auth import get_user_model
from django.db.models import Count, OuterRef, Subquery
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.constants.drf_action import DRFAction
from task_manager.constants.project import ProjectRole
from task_manager.models import Project, ProjectMember
from task_manager.permissions.project import IsProjectAdmin
from task_manager.serializers.project import (ProjectDetailSerializer, ProjectNewMemberSerializer, ProjectSerializer,
                                              ProjectUpdateMemberRole)

User = get_user_model()


@extend_schema(tags=['Project'])
class ProjectViewSet(viewsets.ModelViewSet):
    lookup_field = 'key'
    lookup_url_kwarg = 'project_key'

    def perform_create(self, serializer) -> None:
        project = serializer.save()
        ProjectMember.objects.create(project=project, member=self.request.user, role=ProjectRole.ADMIN)

    def get_serializer_class(self):
        if self.action == DRFAction.RETRIEVE:
            return ProjectDetailSerializer
        return ProjectSerializer

    def get_queryset(self):
        projects_of_auth_user = ProjectMember.objects.filter(member=self.request.user).values('project')
        members_counter = ProjectMember.objects \
            .filter(project=OuterRef('id')) \
            .values('project') \
            .annotate(total=Count('*')) \
            .values('total')
        return Project.objects \
            .filter(id__in=Subquery(projects_of_auth_user)) \
            .annotate(members_counter=Subquery(members_counter))

    def get_permissions(self):
        match self.action:
            case DRFAction.UPDATE | DRFAction.PARTIAL_UPDATE | DRFAction.DESTROY:
                return [IsAuthenticated(), IsProjectAdmin()]
            case _:
                return [IsAuthenticated()]


@extend_schema(tags=['Project'], responses={status.HTTP_200_OK: ProjectDetailSerializer})
class ProjectAddMemberView(generics.CreateAPIView):
    serializer_class = ProjectNewMemberSerializer
    permission_classes = [IsAuthenticated, IsProjectAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'project_key': kwargs['project_key']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ProjectDetailSerializer(serializer.project).data)


@extend_schema(tags=['Project'], responses=ProjectDetailSerializer)
class ProjectMemberView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsProjectAdmin]
    serializer_class = ProjectUpdateMemberRole

    def get_project_member(self, request, *args, **kwargs):  # pylint: disable=W0613
        project_key = kwargs.get('project_key')
        project = get_object_or_404(Project, key=project_key)

        member_id = kwargs.get('member_id')
        member = get_object_or_404(User, id=member_id)

        project_member = get_object_or_404(ProjectMember, project=project, member=member)

        return project, member, project_member

    def update(self, request, *args, **kwargs):
        project, _, project_member = self.get_project_member(self, request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=project_member)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ProjectDetailSerializer(project).data)

    def delete(self, request, *args, **kwargs):
        _, _, project_member = self.get_project_member(self, request, *args, **kwargs)
        project_member.delete()
        return Response()
