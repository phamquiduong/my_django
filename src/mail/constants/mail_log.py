from enum import StrEnum


class MailLogStatus(StrEnum):
    PENDING = 'pending'
    SENDING = 'sending'
    SENT = 'sent'
    FAILED = 'failed'
