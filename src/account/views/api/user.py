from enum import StrEnum
from http import HTTPMethod

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from account.serializers.user import (ChangePasswordSerializer, SendVerifyEmail, UserDetailSerializer,
                                      UserRegisterSerializer, UserSerializer, UserUpdateByAdminSerializer,
                                      UserUpdateProfileSerializer, VerifyEmailByCode)
from common.constants.drf_action import DRFAction

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
        VERIFY_EMAIL_BY_CODE = 'verify_email_by_code'

    def get_permissions(self):
        match self.action:
            case (self.Action.ME | self.Action.PROFILE | self.Action.CHANGE_PASSWORD |
                  self.Action.SEND_VERIFY_EMAIL | self.Action.VERIFY_EMAIL_BY_CODE):
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
            case self.Action.VERIFY_EMAIL_BY_CODE:
                return VerifyEmailByCode
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

    @extend_schema(responses={status.HTTP_202_ACCEPTED: SendVerifyEmail})
    @action(detail=False, url_path='send-verify-email', methods=[HTTPMethod.POST])
    def send_verify_email(self, request: Request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Email queued'}, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, url_path='verify-email-by-code', methods=[HTTPMethod.PATCH])
    def verify_email_by_code(self, request: Request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Email verified'})
