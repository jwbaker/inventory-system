from django import forms
from django.contrib.auth.models import User

from uw_forms import widgets


class UserForm(forms.ModelForm):
    FIELD_LIST = [
        {'Name': 'first_name'},
        {'Name': 'last_name'}
    ]

    INSTANCE_MEMBER = 'username'

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
        ]
        widgets = {
            'first_name': widgets.TextInput({
                'id': 'inputFirstName',
                'placeholder': 'firstName',
            }),
            'last_name': widgets.TextInput({
                'id': 'inputLastName',
                'placeholder': 'lastName',
            }),
        }
