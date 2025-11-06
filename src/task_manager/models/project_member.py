from django.contrib.auth import get_user_model
from django.db import models

from common.models.base import TimestampMixin
from task_manager.constants.project import ProjectRole
from task_manager.models.project import Project

User = get_user_model()


class ProjectMember(TimestampMixin):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=15, choices=ProjectRole.choices(), default=ProjectRole.MEMBER)

    class Meta:
        unique_together = ['project', 'member']
