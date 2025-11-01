from django import forms
from django.contrib.auth import get_user_model

from account.forms._fields import PASSWORD_FIELD

User = get_user_model()


class ChangePasswordForm(forms.Form):
    current_password = PASSWORD_FIELD
    new_password = PASSWORD_FIELD

    def __init__(self, *args, user: User, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password", "")

        if not self.user.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")

        return current_password

    def save(self) -> User:
        new_password = self.cleaned_data["new_password"]

        self.user.set_password(new_password)
        self.user.save()

        return self.user
