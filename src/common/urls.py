from django.urls import include, path
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from common.views import home_view


@extend_schema(exclude=True)
class HiddenSpectacularAPIView(SpectacularAPIView):
    pass


api = [
    path('schema/', HiddenSpectacularAPIView.as_view(), name='api_schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api_schema'), name='swagger-ui'),
    path('re-doc/', SpectacularRedocView.as_view(url_name='api_schema'), name='redoc'),
]


urlpatterns = [
    path('api/', include(api)),
    path('', home_view, name='home'),
]
