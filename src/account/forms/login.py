from django import forms
from django.contrib.auth import get_user_model

from account.forms._fields import PASSWORD_FIELD, USERNAME_FIELD

User = get_user_model()


class LoginForm(forms.Form):
    username = USERNAME_FIELD
    password = PASSWORD_FIELD

    user: User | None = None

    def clean_username(self):
        username = self.cleaned_data["username"].lower()

        self.user = User.objects.filter(username__iexact=username).first()

        if not self.user:
            raise forms.ValidationError("User does not exist.")

        return username

    def clean_password(self):
        password = self.cleaned_data["password"]

        if self.user and not self.user.check_password(raw_password=password):
            raise forms.ValidationError("Password incorrect.")

        return password
