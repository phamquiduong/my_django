from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from rest_framework import serializers

from account.serializers.province import ProvinceSerializer
from account.serializers.ward import WardSerializer
from account.utils.generate_otp import generate_otp
from common.services.dynamodb import get_dynamodb_service
from mail.schemas.mail import MailLog
from mail.tasks.send_mail import send_email_async_task

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


class SendVerifyEmail(serializers.Serializer):
    detail = serializers.CharField(default='Email queued', read_only=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if user.email_verified is True:
            raise serializers.ValidationError('User email is verified')

        if not user.email:
            raise serializers.ValidationError('User does not include email')

        if cache.get(f'verify-email-otp:{user.id}') is not None:
            raise serializers.ValidationError('An email sent. Please check your inbox')

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user

        otp = generate_otp()
        cache.set(f'verify-email-otp:{user.id}', otp, timeout=settings.OTP_TIMEOUT)

        mail_log = MailLog(
            to=[user.email],
            subject='Verify your email',
            template_name='verify_email',
            context={
                'otp': otp,
            }
        )

        with get_dynamodb_service() as dynamodb_service:
            mail_log.create(dynamodb_service)

        send_email_async_task.apply_async(task_id=mail_log.task_id)  # type:ignore

        return mail_log

    def update(self, instance, validated_data):
        pass


class VerifyEmailByCode(serializers.Serializer):
    detail = serializers.CharField(default='Email verified', read_only=True)

    code = serializers.RegexField(regex=r'\d*', max_length=6, min_length=6, write_only=True)

    def validate_code(self, code: str) -> str:
        user = self.context['request'].user
        user_code = cache.get(f'verify-email-otp:{user.id}')

        if user_code != code:
            raise serializers.ValidationError('Invalid verify code')

        return code

    def create(self, validated_data):
        user = self.context['request'].user
        user.email_verified = True
        user.save(update_fields=['email_verified'])

        cache.delete(f'verify-email-otp:{user.id}')

        return user

    def update(self, instance, validated_data):
        pass
