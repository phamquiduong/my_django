import logging
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, ClassVar

from common.services.dynamodb import DynamoDBService
from mail.constants.mail_log import MailLogStatus

logger = logging.getLogger(__name__)


@dataclass
class MailLog:
    table_name: ClassVar[str] = 'mail_log'

    to: list[str]
    subject: str

    template_name: str
    context: dict[str, Any] | None = None

    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: MailLogStatus = MailLogStatus.PENDING
    error: str | None = None

    def create(self, dynamodb_service: DynamoDBService):
        dynamodb_service.insert(table_name=self.table_name, data=asdict(self))

    def update_status(self, dynamodb_service: DynamoDBService, status: MailLogStatus):
        response = dynamodb_service.update(
            table_name=self.table_name,
            query={'task_id': self.task_id},
            expression='SET #s = :new_status',
            expression_name={'#s': 'status'},
            expression_value={':new_status': status}
        )
        logger.info('Status updated: %s', response)

    def set_error(self,  dynamodb_service: DynamoDBService, detail: str):
        response = dynamodb_service.update(
            table_name=self.table_name,
            query={'task_id': self.task_id},
            expression='SET #s = :new_status, #err = :detail',
            expression_name={
                '#s': 'status',
                '#err': 'error',
            },
            expression_value={
                ':new_status': MailLogStatus.FAILED,
                ':detail': detail
            }
        )
        logger.info('Status updated: %s', response)
