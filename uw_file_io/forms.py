from django import forms


class ImportForm(forms.Form):
    file_up = forms.FileField(required=True)
    model = forms.ChoiceField(
        choices=(
            ('II', 'Inventory Items'),
        ),
        label='Record kind'
    )
