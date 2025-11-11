import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, ClassVar

from common.services.dynamodb import DynamoDBService
from mail.constants.mail_log import MailLogStatus
from mail.utils.mail_log import delete_after_factory, time_now_factory


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

    created_at: int = field(default_factory=time_now_factory)
    updated_at: int = field(default_factory=time_now_factory)
    delete_after: int = field(default_factory=delete_after_factory)

    def create(self, dynamodb_service: DynamoDBService):
        dynamodb_service.insert(table_name=self.table_name, data=asdict(self))

    def update_status(self, dynamodb_service: DynamoDBService, status: MailLogStatus):
        dynamodb_service.update(
            table_name=self.table_name,
            query={'task_id': self.task_id},
            expression='SET #status = :new_status, #updated_at = :time_now',
            expression_name={
                '#status': 'status',
                '#updated_at': 'updated_at',
            },
            expression_value={
                ':new_status': status,
                ':time_now': time_now_factory(),
            }
        )

    def set_error(self,  dynamodb_service: DynamoDBService, detail: str):
        dynamodb_service.update(
            table_name=self.table_name,
            query={'task_id': self.task_id},
            expression='SET #status = :new_status, #err = :detail, #updated_at = :time_now',
            expression_name={
                '#status': 'status',
                '#err': 'error',
                '#updated_at': 'updated_at',
            },
            expression_value={
                ':new_status': MailLogStatus.FAILED,
                ':detail': detail,
                ':time_now': time_now_factory(),
            }
        )
