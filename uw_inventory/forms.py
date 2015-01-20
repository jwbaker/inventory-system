from django import forms

from uw_inventory import widgets
from uw_inventory.models import InventoryItem, InventoryItemLocation


class ItemForm(forms.ModelForm):
    FIELD_LIST = [
        {'Name': 'name',                  'Type': 'text'},
        {'Name': 'description',           'Type': 'textarea'},
        {'Name': 'status',                'Type': 'dropdown'},
        {'Name': 'location',              'Type': 'autocomplete'},
        {'Name': 'manufacture_date',      'Type': 'date'},
        {'Name': 'purchase_price',        'Type': 'currency'},
        {'Name': 'purchase_date',         'Type': 'date'},
        {'Name': 'replacement_cost',      'Type': 'currency'},
        {'Name': 'replacement_cost_date', 'Type': 'date'},
        {'Name': 'csa_required',          'Type': 'boolean'},
        {'Name': 'factory_csa',           'Type': 'boolean'},
        {'Name': 'csa_special',           'Type': 'boolean'},
        {'Name': 'csa_special_date',      'Type': 'date'},
        {'Name': 'modified_since_csa',    'Type': 'boolean'},
        {'Name': 'undergraduate',         'Type': 'boolean'},
        {'Name': 'csa_cost',              'Type': 'currency'},
        {'Name': 'lifting_device',        'Type': 'boolean'},
    ]

    class Meta:
        model = InventoryItem
        exclude = ['deleted']
        labels = {
            'csa_cost': 'CSA certification cost',
            'csa_required': 'CSA required?',
            'csa_special': 'Special CSA inspection?',
            'csa_special_date': 'CSA inspection date',
            'factory_csa': 'Factory CSA certification?',
            'lifting_device': 'Lifting device?',
            'modified_since_csa': 'Modified since inspection?',
            'replacement_cost_date': 'Estimation date',
            'undergraduate': 'Used for undergrad teaching?',
        }
        widgets = {
            'csa_cost': forms.NumberInput(attrs={
                'id': 'inputCsaCost',
                'class': 'form-control form-element',
                'placeholder': 0,
            }),
            'csa_required': widgets.CheckboxInput(attrs={
                'id': 'inputCsaRequired',
                'class': 'item-input form-element',
            }),
            'csa_special': widgets.CheckboxInput(attrs={
                'id': 'inputCsaSpecial',
                'class': 'item-input form-element',
            }),
            'csa_special_date': widgets.DateInput(attrs={
                'id': 'inputCsaSpecialDate',
                'class': 'form-control item-input form-element',
            }),
            'description': forms.Textarea(attrs={
                'id': 'inputDescription',
                'class': 'form-control item-input form-element',
                'placeholder': 'Description',
                'rows': '5',  # Arbitrary number is arbitrary
                'style': 'resize:vertical',  # Horizontal resizing kills layout
            }),
            'factory_csa': widgets.CheckboxInput(attrs={
                'id': 'inputFactoryCsa',
                'class': 'item-input form-element',
            }),
            'lifting_device': widgets.CheckboxInput(attrs={
                'id': 'inputLiftingDevice',
                'class': 'item-input form-element',
            }),
            'location': widgets.AutocompleteInput(attrs={
                'id': 'inputLocation',
                'class': 'form-control item-input form-element',
                'placeholder': 'Begin typing the location...',
                'data-set': InventoryItemLocation.objects
            }),
            'manufacture_date': widgets.DateInput(attrs={
                'id': 'inputManufactureDate',
                'class': 'form-control item-input form-element',
            }),
            'modified_since_csa': widgets.CheckboxInput(attrs={
                'id': 'inputModifiedSinceCsa',
                'class': 'item-input form-element',
            }),
            'name': forms.TextInput(attrs={
                'id': 'inputName',
                'class': 'form-control item-input form-element',
                'placeholder': 'Name',
            }),
            'purchase_date': widgets.DateInput(attrs={
                'id': 'inputPurchaseDate',
                'class': 'form-control item-input form-element',
            }),
            'purchase_price': forms.NumberInput(attrs={
                'id': 'inputStatus',
                # .item-input will be added to the container div
                'class': 'form-control form-element',
                'placeholder': 0,
            }),
            'replacement_cost': forms.NumberInput(attrs={
                'id': 'inputReplacementCost',
                'class': 'form-control form-element',
                'placeholder': 0,
            }),
            'replacement_cost_date': widgets.DateInput(attrs={
                'id': 'inputReplacementCostDate',
                'class': 'form-control item-input form-element',
            }),
            'status': forms.Select(attrs={
                'id': 'inputStatus',
                'class': 'form-control item-input form-element',
            }),
            'undergraduate': widgets.CheckboxInput(attrs={
                'id': 'inputUndergraduate',
                'class': 'item-input form-element',
            }),
        }
