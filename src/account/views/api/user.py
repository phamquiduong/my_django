from http import HTTPMethod

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from account.serializers.user import (ChangePasswordSerializer, UserDetailSerializer, UserRegisterSerializer,
                                      UserSerializer, UserUpdateByAdminSerializer)

User = get_user_model()


@extend_schema(tags=['User'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    filterset_fields = ('is_staff', 'is_active', 'email_verified', 'phone_number_verified', 'province', 'ward')

    ordering_fields = ('id', 'username', 'email', 'last_login')
    ordering = ('id',)

    search_fields = ('username', 'email')

    def get_permissions(self):
        if self.action in ['me', 'change_password']:
            return [IsAuthenticated()]
        if self.request.method not in SAFE_METHODS:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'change_password':
            return ChangePasswordSerializer
        if self.action == 'create':
            return UserRegisterSerializer
        if self.action == 'update':
            return UserUpdateByAdminSerializer
        if self.action in ['retrieve', 'me']:
            return UserDetailSerializer
        return UserSerializer

    @action(detail=False, methods=[HTTPMethod.GET])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, url_path='change-password', methods=[HTTPMethod.PATCH])
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
