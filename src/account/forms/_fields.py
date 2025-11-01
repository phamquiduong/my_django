from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator

USERNAME_FIELD = forms.CharField(min_length=4, max_length=32, validators=[UnicodeUsernameValidator()])
PASSWORD_FIELD = forms.CharField(min_length=6, max_length=32, validators=[validate_password])
