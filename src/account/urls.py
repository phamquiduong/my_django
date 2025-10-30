from django.urls import include, path

from account.views.api.auth import LoginAPIView, LogoutAPIView, RefreshTokenAPIView, VerifyTokenAPIView

api = [
    path('login', LoginAPIView.as_view(), name='auth_login_api'),
    path('refresh', RefreshTokenAPIView.as_view(), name='auth_refresh_api'),
    path('verify', VerifyTokenAPIView.as_view(), name='auth_verify_api'),
    path('logout', LogoutAPIView.as_view(), name='auth_logout_api'),
]

urlpatterns = [
    path('api/', include(api)),
]
