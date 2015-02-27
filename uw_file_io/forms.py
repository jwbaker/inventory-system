from django import forms


class ImportForm(forms.Form):
    file_up = forms.FileField()
