from django import forms
from django.contrib.auth import get_user_model

from account.forms._fields import PASSWORD_FIELD, USERNAME_FIELD

User = get_user_model()


class RegisterForm(forms.Form):
    username = USERNAME_FIELD
    password = PASSWORD_FIELD

    def clean_username(self) -> str:
        username = self.cleaned_data["username"].lower()

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This account already exist.")

        return username

    def save(self) -> User:
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
        )
        return user
