from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView, TokenVerifyView


@extend_schema(tags=["Authentication"])
class LoginAPIView(TokenObtainPairView):
    pass


@extend_schema(tags=["Authentication"])
class LogoutAPIView(TokenBlacklistView):
    pass


@extend_schema(tags=["Authentication"])
class RefreshTokenAPIView(TokenRefreshView):
    pass


@extend_schema(tags=["Authentication"])
class VerifyTokenAPIView(TokenVerifyView):
    pass
