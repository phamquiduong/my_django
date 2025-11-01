from django.contrib.auth.views import LogoutView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from account.views.api.auth import LoginAPIView, LogoutAPIView, RefreshTokenAPIView, VerifyTokenAPIView
from account.views.api.location import ProvinceViewSet, WardViewSet
from account.views.api.user import UserViewSet
from account.views.change_password import change_password_view
from account.views.login import login_view
from account.views.register import register_view

router = DefaultRouter()
router.register('users', UserViewSet, basename='account_users_api')
router.register('provinces', ProvinceViewSet, basename='account_provinces_api')
router.register('wards', WardViewSet, basename='account_wards_api')

api = [
    path('login', LoginAPIView.as_view(), name='account_login_api'),
    path('refresh', RefreshTokenAPIView.as_view(), name='account_refresh_api'),
    path('verify', VerifyTokenAPIView.as_view(), name='account_verify_api'),
    path('logout', LogoutAPIView.as_view(), name='account_logout_api'),

    path('', include(router.urls)),
]

urlpatterns = [
    path('api/', include(api)),
    path('register', register_view, name='account_register'),
    path('login', login_view, name='account_login'),
    path('logout', LogoutView.as_view(next_page='home'), name='account_logout'),
    path('change-password', change_password_view, name='account_change_password'),
]
