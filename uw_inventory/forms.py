from django import forms

from uw_inventory import widgets
from uw_inventory.models import InventoryItem, InventoryItemLocation


class ItemForm(forms.ModelForm):
    FIELD_LIST = [
        {'Name': 'name'},
        {'Name': 'description'},
        {'Name': 'status'},
        {'Name': 'location'},
        {'Name': 'manufacture_date'},
        {'Name': 'purchase_price'},
        {'Name': 'purchase_date'},
        {'Name': 'replacement_cost'},
        {'Name': 'replacement_cost_date'},
        {'Name': 'csa_required'},
        {'Name': 'factory_csa'},
        {'Name': 'csa_special'},
        {'Name': 'csa_special_date'},
        {'Name': 'modified_since_csa'},
        {'Name': 'undergraduate'},
        {'Name': 'csa_cost'},
        {'Name': 'lifting_device'},
    ]

    class Meta:
        model = InventoryItem
        exclude = ['creation_date', 'deleted']
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
            'csa_cost': widgets.CurrencyInput({'id': 'inputCsaCost'}),
            'csa_required': widgets.CheckboxInput({
                'id': 'inputCsaRequired'
            }),
            'csa_special': widgets.CheckboxInput({
                'id': 'inputCsaSpecial',
            }),
            'csa_special_date': widgets.DateInput({
                'id': 'inputCsaSpecialDate',
            }),
            'description': widgets.TextareaInput({
                'id': 'inputDescription',
                'placeholder': 'Description',
            }),
            'factory_csa': widgets.CheckboxInput({
                'id': 'inputFactoryCsa',
            }),
            'lifting_device': widgets.CheckboxInput({
                'id': 'inputLiftingDevice',
            }),
            'location': widgets.AutocompleteInput({
                'id': 'inputLocation',
                'placeholder': 'Begin typing the location...',
                'data-set': InventoryItemLocation.objects
            }),
            'manufacture_date': widgets.DateInput({
                'id': 'inputManufactureDate',
            }),
            'modified_since_csa': widgets.CheckboxInput({
                'id': 'inputModifiedSinceCsa',
            }),
            'name': widgets.TextInput({
                'id': 'inputName',
                'placeholder': 'Name',
            }),
            'purchase_date': widgets.DateInput({
                'id': 'inputPurchaseDate',
            }),
            'purchase_price': widgets.CurrencyInput({
                'id': 'inputPurchasePrice'
            }),
            'replacement_cost': widgets.CurrencyInput({
                'id': 'inputReplacementCost'
            }),
            'replacement_cost_date': widgets.DateInput({
                'id': 'inputReplacementCostDate',
            }),
            'status': widgets.SelectInput({
                'id': 'inputStatus',
                'translator': InventoryItem.get_status_display,
            }),
            'undergraduate': widgets.CheckboxInput({
                'id': 'inputUndergraduate',
            }),
        }
