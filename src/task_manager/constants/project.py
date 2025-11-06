from common.constants.base import ChoicesEnum


class ProjectRole(str, ChoicesEnum):
    ADMIN = 'admin'
    MEMBER = 'member'
