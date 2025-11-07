from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from account.serializers.province import ProvinceSerializer
from account.serializers.ward import WardSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions')
        extra_kwargs = {
            # Hide password field
            'password': {'write_only': True},

            # Not modify verified info
            'phone_number_verified': {'read_only': True},
            'email_verified': {'read_only': True},

            # Auto generate datetime
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
        }

    def validate_ward(self, ward):
        province_id = self.initial_data.get('province')  # type:ignore
        if ward and province_id and str(ward.province_id) != str(province_id):
            raise serializers.ValidationError('Ward does not belong to the selected province')
        return ward

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(UserSerializer):
    province_detail = ProvinceSerializer(source='province', read_only=True)
    ward_detail = WardSerializer(source='ward', read_only=True)

    class Meta(UserSerializer.Meta):
        extra_kwargs = UserSerializer.Meta.extra_kwargs.copy()
        extra_kwargs.update({
            'province': {'write_only': True},
            'ward': {'write_only': True},
        })


class UserRegisterSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        extra_kwargs = UserSerializer.Meta.extra_kwargs.copy()
        extra_kwargs.update({
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
        })


class UserUpdateByAdminSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        exclude = ('password', *UserSerializer.Meta.exclude)


class UserUpdateProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        exclude = ('password', *UserSerializer.Meta.exclude)
        extra_kwargs = UserSerializer.Meta.extra_kwargs.copy()
        extra_kwargs.update({
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
        })


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    detail = serializers.CharField(read_only=True, default='Password changed successfully')

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Old password is incorrect.')
        return old_password

    def validate_new_password(self, new_password):
        old_password = self.initial_data.get('old_password')  # type:ignore
        if old_password and new_password and old_password == new_password:
            raise serializers.ValidationError('New password is the same as old password')

        validate_password(new_password, self.context['request'].user)
        return new_password

    def create(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):  # pylint: disable=W0613
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])  # type:ignore
        user.save()
        return user
