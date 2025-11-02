from http import HTTPMethod

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from account.serializers.user import ChangePasswordSerializer, UserCreateSerializer, UserUpdateByAdminSerializer

User = get_user_model()


@extend_schema(tags=["User"])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    filterset_fields = ("is_staff", "is_active", "email_verified", "phone_number_verified", "province", "ward")

    ordering_fields = ("id", "username", "email", "last_login")
    ordering = ("id",)

    search_fields = ("username", "email")

    def get_permissions(self):
        if self.action in ["me", "change_password"]:
            return [IsAuthenticated()]
        if self.request.method in [HTTPMethod.PUT, HTTPMethod.PATCH, HTTPMethod.DELETE]:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == "change_password":
            return ChangePasswordSerializer
        if self.request.method == HTTPMethod.POST:
            return UserCreateSerializer
        return UserUpdateByAdminSerializer

    @action(detail=False, methods=[HTTPMethod.GET])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, url_path="change-password", methods=[HTTPMethod.PATCH], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
