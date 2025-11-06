from enum import Enum


class ChoicesEnum(Enum):
    @classmethod
    def choices(cls):
        return [(member.value, member.name.title()) for member in cls]
