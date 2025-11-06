import base64
import uuid

from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDPrimaryMixin(models.Model):
    # Will upgrade to UUID7 when the System upgrade to PostgreSQL18 and Python3.14
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    @property
    def id_display(self) -> str | None:
        return base64.urlsafe_b64encode(self.id.bytes).decode('utf-8').rstrip('=') if self.id else None

    class Meta:
        abstract = True
