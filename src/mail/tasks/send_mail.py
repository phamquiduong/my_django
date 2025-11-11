import logging
import traceback

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from common.services.dynamodb import get_dynamodb_service
from mail.constants.mail_log import MailLogStatus
from mail.schemas.mail import MailLog

logger = logging.getLogger(__name__)


@shared_task(bind=True, queue='email')
def send_email_async_task(self):
    task_id = self.request.id

    with get_dynamodb_service() as dynamodb_service:
        response = dynamodb_service.get(MailLog.table_name, {'task_id': task_id})
        email_log = MailLog(**response)
        email_log.update_status(dynamodb_service, status=MailLogStatus.SENDING)

    html_content = render_to_string(f'mail/{email_log.template_name}.html', context=email_log.context)

    msg = EmailMessage(
        subject=email_log.subject,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email_log.to,
    )
    msg.content_subtype = 'html'

    try:
        msg.send()
    except Exception:
        with get_dynamodb_service() as dynamodb_service:
            email_log.set_error(dynamodb_service, detail=traceback.format_exc())
        raise

    with get_dynamodb_service() as dynamodb_service:
        email_log.update_status(dynamodb_service, status=MailLogStatus.SENT)
