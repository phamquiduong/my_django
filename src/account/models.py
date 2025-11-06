from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as AbstractUserManager
from django.db import models

from common.models.base import TimestampMixin


class Province(models.Model):
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    full_name_en = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.name}'


class Ward(models.Model):
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    full_name_en = models.CharField(max_length=255)

    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name}'


class UserManager(AbstractUserManager):
    @classmethod
    def normalize_email(cls, email):
        if email is None:
            return None
        return super().normalize_email(email)


class User(AbstractUser, TimestampMixin):
    # Remove some fields
    first_name = None
    last_name = None

    display_name = models.CharField(max_length=128, default='User')

    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    phone_number_verified = models.BooleanField(default=False)

    email = models.EmailField(unique=True, null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)

    objects = UserManager()

    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f'<User: {self.username}>'
