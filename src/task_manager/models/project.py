from django.db import models

from common.models.base import TimestampMixin


class ProjectManager(models.Manager):
    def create(self, **kwargs):
        obj = super().create(**kwargs)
        if 'key' not in kwargs:
            obj.key = f'PRJ-{obj.id}'
            obj.save()
        return obj


class Project(TimestampMixin):
    key = models.CharField(max_length=32, unique=True, blank=True, null=True)

    name = models.CharField(max_length=255)

    objects = ProjectManager()
