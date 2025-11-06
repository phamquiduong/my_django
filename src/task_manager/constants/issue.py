from common.constants.base import ChoicesEnum


class IssueStatus(str, ChoicesEnum):
    OPEN = 'open'
    IN_PROCESS = 'in_progress'
    DONE = 'done'
