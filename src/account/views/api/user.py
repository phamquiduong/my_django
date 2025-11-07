from enum import StrEnum
from http import HTTPMethod

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from account.serializers.user import (ChangePasswordSerializer, UserDetailSerializer, UserRegisterSerializer,
                                      UserSerializer, UserUpdateByAdminSerializer, UserUpdateProfileSerializer)
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

    def get_permissions(self):
        match self.action:
            case self.Action.ME | self.Action.PROFILE | self.Action.CHANGE_PASSWORD:
                return [IsAuthenticated()]
            case DRFAction.UPDATE | DRFAction.PARTIAL_UPDATE | DRFAction.DESTROY:
                return [IsAdminUser()]
            case _:
                return [AllowAny()]

    def get_serializer_class(self):
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
