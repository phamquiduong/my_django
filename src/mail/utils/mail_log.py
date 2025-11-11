from datetime import datetime

from django.conf import settings
from django.utils import timezone


def delete_after_factory() -> int:
    delete_after: datetime = timezone.now() + settings.MAIL_LOG_EXPIRED
    return int(delete_after.timestamp())


def time_now_factory() -> int:
    return int(timezone.now().timestamp())
