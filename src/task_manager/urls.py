from django.urls import include, path
from rest_framework.routers import DefaultRouter

from task_manager.views.api.project import ProjectMemberView, ProjectViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='task_manager_projects')


api = [
    path('', include(router.urls)),
    path('projects/<str:project_key>/members', ProjectMemberView.as_view()),
]

urlpatterns = [
    path('api/', include(api)),
]
