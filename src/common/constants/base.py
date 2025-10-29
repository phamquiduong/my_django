from enum import Enum


class ChoicesEnum(Enum):
    @classmethod
    def choices(cls):
        return [(member.value, member.name) for member in cls]
