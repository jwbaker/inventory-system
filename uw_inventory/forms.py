from django import forms

from uw_inventory.models import InventoryItem


# We need this class because Django's default date widget is a text box
class DateInput(forms.DateInput):
    input_type = 'date'


class ItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        exclude = ['deleted']
        widgets = {
            'description': forms.Textarea(attrs={
                'id': 'inputDescription',
                'class': 'form-control item-input',
                'placeholder': 'Description',
                'rows': '5',  # Arbitrary number is arbitrary
                'style': 'resize:vertical',  # Horizontal resizing kills layout
            }),
            'manufacture_date': DateInput(attrs={
                'id': 'inputManufactureDate',
                'class': 'form-control item-input',
            }),
            'name': forms.TextInput(attrs={
                'id': 'inputName',
                'class': 'form-control item-input',
                'placeholder': 'Name',
            }),
            'purchase_date': DateInput(attrs={
                'id': 'inputPurchaseDate',
                'class': 'form-control item-input'
            }),
            'purchase_price': forms.NumberInput(attrs={
                'id': 'inputStatus',
                # .item-input will be added to the container div
                'class': 'form-control',
                'placeholder': 0,
            }),
            'status': forms.Select(attrs={
                'id': 'inputStatus',
                'class': 'form-control item-input',
            }),
        }
