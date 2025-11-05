import logging

from django import forms
from django.contrib.auth import get_user_model

from account.models import Province, Ward

User = get_user_model()
logger = logging.getLogger()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'display_name', 'phone_number', 'email', 'province', 'ward']

    def clean_ward(self):
        province: Province | None = self.cleaned_data.get('province')
        ward: Ward | None = self.cleaned_data.get('ward')

        if province and ward and ward.province != province:
            raise forms.ValidationError('Ward not belong to Province')

        return ward
