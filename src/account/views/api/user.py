from enum import StrEnum
from http import HTTPMethod

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from account.serializers.user import (ChangePasswordSerializer, SendVerifyEmail, UserDetailSerializer,
                                      UserRegisterSerializer, UserSerializer, UserUpdateByAdminSerializer,
                                      UserUpdateProfileSerializer)
from common.constants.drf_action import DRFAction
from common.services.dynamodb import get_dynamodb_service
from mail.schemas.mail import MailLog
from mail.tasks.send_mail import send_email_async_task

User = get_user_model()


@extend_schema(tags=['User'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    filterset_fields = ('is_staff', 'is_active', 'email_verified', 'phone_number_verified', 'province', 'ward')

    ordering_fields = ('id', 'username', 'email', 'last_login')
    ordering = ('id',)

    search_fields = ('username', 'email')

    class Action(StrEnum):
        ME = 'me'
        PROFILE = 'profile'
        CHANGE_PASSWORD = 'change_password'
        SEND_VERIFY_EMAIL = 'send_verify_email'

    def get_permissions(self):
        match self.action:
            case self.Action.ME | self.Action.PROFILE | self.Action.CHANGE_PASSWORD | self.Action.SEND_VERIFY_EMAIL:
                return [IsAuthenticated()]
            case DRFAction.UPDATE | DRFAction.PARTIAL_UPDATE | DRFAction.DESTROY:
                return [IsAdminUser()]
            case _:
                return [AllowAny()]

    def get_serializer_class(self):  # pylint: disable=R0911
        match self.action:
            case DRFAction.CREATE:
                return UserRegisterSerializer
            case DRFAction.UPDATE | DRFAction.PARTIAL_UPDATE:
                return UserUpdateByAdminSerializer
            case DRFAction.RETRIEVE | self.Action.ME:
                return UserDetailSerializer
            case self.Action.CHANGE_PASSWORD:
                return ChangePasswordSerializer
            case self.Action.PROFILE:
                return UserUpdateProfileSerializer
            case self.Action.SEND_VERIFY_EMAIL:
                return SendVerifyEmail
            case _:
                return UserSerializer

    @action(detail=False, methods=[HTTPMethod.GET])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=[HTTPMethod.PUT, HTTPMethod.PATCH])
    def profile(self, request: Request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, url_path='change-password', methods=[HTTPMethod.PATCH])
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password changed successfully'})

    @action(detail=False, url_path='send-verify-email', methods=[HTTPMethod.POST])
    def send_verify_email(self, request: Request):
        if request.user.email_verified is True:
            raise ValidationError('User email is verified')

        if not request.user.email:
            raise ValidationError('User does not include email')

        mail_log = MailLog(
            to=[request.user.email],
            subject='Verify your email',
            template_name='verify_email',
        )

        with get_dynamodb_service() as dynamodb_service:
            mail_log.create(dynamodb_service)

        send_email_async_task.apply_async(task_id=mail_log.task_id)  # type:ignore

        return Response({'detail': 'Please check your inbox. If you don\'t receive any email, please contact to Admin'})
