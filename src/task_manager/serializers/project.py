from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from account.serializers.user import UserSerializer
from task_manager.constants.project import ProjectRole
from task_manager.models import Project
from task_manager.models.project_member import ProjectMember

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    members_counter = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectMemberSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['member', 'role']


class ProjectNewMemberSerializer(serializers.Serializer):
    member_id = serializers.IntegerField(write_only=True)
    member: User    # type:ignore
    project: Project

    def validate_member_id(self, member_id):
        try:
            self.member = User.objects.get(id=member_id)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError('Member does not exist') from exc

        if ProjectMember.objects.filter(project=self.project, member=self.member).exists():
            raise serializers.ValidationError('The member already in project')

        return member_id

    def validate(self, attrs):
        project_key = self.context['project_key']

        try:
            self.project = Project.objects.get(key=project_key)
        except Project.DoesNotExist as exc:
            raise serializers.ValidationError('Project does not exist') from exc

        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return ProjectMember.objects.create(project=self.project, member=self.member)


class ProjectUpdateMemberRole(serializers.Serializer):
    role = serializers.ChoiceField(choices=ProjectRole.choices())

    def update(self, instance, validated_data):
        instance.role = validated_data['role']
        instance.save(update_fields=['role'])
        return instance

    def create(self, validated_data):
        pass


class ProjectDetailSerializer(ProjectSerializer):
    members = serializers.SerializerMethodField()

    @extend_schema_field(ProjectMemberSerializer(many=True, read_only=True))
    def get_members(self, obj):
        project_members = ProjectMember.objects.filter(project=obj)
        return ProjectMemberSerializer(project_members, many=True).data
