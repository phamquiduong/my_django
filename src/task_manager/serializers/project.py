from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from account.serializers.user import UserSerializer
from task_manager.models import Project
from task_manager.models.project_member import ProjectMember


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectMemberSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['member', 'role']


class ProjectDetailSerializer(ProjectSerializer):
    members = serializers.SerializerMethodField()

    @extend_schema_field(ProjectMemberSerializer(many=True, read_only=True))
    def get_members(self, obj):
        project_members = ProjectMember.objects.filter(project=obj)
        return ProjectMemberSerializer(project_members, many=True).data
