from enum import StrEnum


class DRFAction(StrEnum):
    LIST = 'list'
    RETRIEVE = 'retrieve'
    CREATE = 'create'
    UPDATE = 'update'
    PARTIAL_UPDATE = 'partial_update'
    DESTROY = 'destroy'
