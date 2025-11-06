from django.contrib.auth import get_user_model
from django.db import models

from common.models.base import TimestampMixin
from task_manager.constants.issue import IssueStatus
from task_manager.models.project import Project

User = get_user_model()


class IssueManager(models.Manager):
    def create(self, **kwargs):
        obj = super().create(**kwargs)
        if 'key' not in kwargs:
            obj.key = f'PRJ-{obj.project.key}-{obj.id}'
            obj.save()
        return obj


class Issue(TimestampMixin):
    key = models.CharField(max_length=32, unique=True, blank=True, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=15, choices=IssueStatus.choices(), default=IssueStatus.OPEN)

    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    objects = IssueManager()
