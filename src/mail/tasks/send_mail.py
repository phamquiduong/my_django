import logging
import traceback

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
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

    html_content = render_to_string(f'mail/{email_log.template_name}.html', email_log.context)

    msg = EmailMultiAlternatives(subject=email_log.subject, to=email_log.to)
    msg.attach_alternative(html_content, 'text/html')

    try:
        msg.send()
    except Exception:
        with get_dynamodb_service() as dynamodb_service:
            email_log.set_error(dynamodb_service, detail=traceback.format_exc())
        raise

    with get_dynamodb_service() as dynamodb_service:
        email_log.update_status(dynamodb_service, status=MailLogStatus.SENT)
