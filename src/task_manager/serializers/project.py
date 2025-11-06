from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from account.serializers.user import UserSerializer
from task_manager.models import Project
from task_manager.models.project_member import ProjectMember

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
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

    new_member: User

    def validate_member_id(self, member_id):
        try:
            self.new_member = User.objects.get(id=member_id)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError('Member ID does not exist') from exc

        if ProjectMember.objects.filter(project=self.instance, member=self.new_member).exists():
            raise serializers.ValidationError('The member already exist')

        return member_id

    def save(self, **kwargs):
        return ProjectMember.objects.create(project=self.instance, member=self.new_member)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ProjectDetailSerializer(ProjectSerializer):
    members = serializers.SerializerMethodField()

    @extend_schema_field(ProjectMemberSerializer(many=True, read_only=True))
    def get_members(self, obj):
        project_members = ProjectMember.objects.filter(project=obj)
        return ProjectMemberSerializer(project_members, many=True).data
