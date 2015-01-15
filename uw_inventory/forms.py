from django import forms

from uw_inventory.models import InventoryItem


class ItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        exclude = ['deleted']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'inputName',
                'class': 'form-control item-input',
                'placeholder': 'Name',
            }),
            'description': forms.Textarea(attrs={
                'id': 'inputDescription',
                'class': 'form-control item-input',
                'placeholder': 'Description',
                'rows': '5',
                'style': 'resize:vertical',
            }),
            'status': forms.Select(attrs={
                'id': 'inputStatus',
                'class': 'form-control item-input',
            }),
            'purchase_price': forms.NumberInput(attrs={
                'id': 'inputStatus',
                'class': 'form-control',
                'placeholder': 0,
            }),
        }
