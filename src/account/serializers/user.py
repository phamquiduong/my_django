from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from account.serializers.province import ProvinceSerializer
from account.serializers.ward import WardSerializer

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    province_detail = ProvinceSerializer(source="province", read_only=True)
    ward_detail = WardSerializer(source="ward", read_only=True)

    class Meta:
        model = User
        extra_kwargs = {
            "password": {"write_only": True},
            "province": {"write_only": True},
            "ward": {"write_only": True},
            "last_login": {"read_only": True},
            "is_superuser": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_active": {"read_only": True},
            "date_joined": {"read_only": True},
            "phone_number_verified": {"read_only": True},
            "email_verified": {"read_only": True},
        }
        exclude = ("groups", "user_permissions")

    def validate_ward(self, ward):
        province_id = self.initial_data.get("province")  # type:ignore
        if ward and province_id and str(ward.province_id) != str(province_id):
            raise serializers.ValidationError("Ward does not belong to the selected province")
        return ward

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateByAdminSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        extra_kwargs = {
            "province": {"write_only": True},
            "ward": {"write_only": True},
            "last_login": {"read_only": True},
            "date_joined": {"read_only": True},
        }
        exclude = ("password", "groups", "user_permissions")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    detail = serializers.CharField(read_only=True, default="Password changed successfully")

    def validate_old_password(self, old_password):
        user = self.context["request"].user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")
        return old_password

    def validate_new_password(self, new_password):
        old_password = self.initial_data.get("old_password")  # type:ignore
        if old_password and new_password and old_password == new_password:
            raise serializers.ValidationError("New password is the same as old password")

        validate_password(new_password, self.context["request"].user)
        return new_password

    def create(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):  # pylint: disable=W0613
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])  # type:ignore
        user.save()
        return user
