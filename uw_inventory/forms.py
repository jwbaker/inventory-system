from django import forms

from uw_inventory import widgets
from uw_inventory.models import (
    AutocompleteData,
    InventoryItem
)


class ItemForm(forms.ModelForm):
    # This list provides metdata to the field renderer.
    # Most of that logic is field order, but legacy fields are also described
    FIELD_LIST = [
        {'Name': 'name'},
        {'Name': 'tech_id', 'Legacy': True},
        {'Name': 'description'},
        {'Name': 'status'},
        {'Name': 'location'},
        {'Name': 'manufacturer'},
        {'Name': 'model_number'},
        {'Name': 'serial_number'},
        {'Name': 'manufacture_date'},
        {'Name': 'supplier'},
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
        {'Name': 'sop_required'},
        {'Name': 'lifting_device'},
        {'Name': 'lifting_device_inspection_date'},
    ]

    class Meta:
        model = InventoryItem
        exclude = ['creation_date', 'deleted', 'last_modified', 'uuid']

        # The labels are only necessary if sentence-casing the field name
        # doesn't work, i.e. abbreviations and punctuation
        labels = {
            'csa_cost': 'CSA certification cost',
            'csa_required': 'CSA required?',
            'csa_special': 'Special CSA inspection required?',
            'csa_special_date': 'Special CSA inspection date',
            'factory_csa': 'Factory CSA certification?',
            'lifting_device': 'Lifting device?',
            'lifting_device_inspection_date': 'Lifting device inspection date',
            'modified_since_csa': 'Modified since CSA inspection?',
            'replacement_cost_date': 'Estimation date',
            'sop_required': 'SOP required?',
            'tech_id': 'Technician ID',
            'undergraduate': 'Used for undergrad teaching?',
        }

        # EVERY field must have a widget defined, and it must be one of our
        # specially-defined widgets, because we rely on every element having
        # certains IDs and classes.
        widgets = {
            'csa_cost': widgets.CurrencyInput({
                'id': 'inputCsaCost'
            }),
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
            'lifting_device_inspection_date': widgets.DateInput({
                'id': 'inputLiftingDeviceInspectionDate',
            }),
            'location': widgets.AutocompleteInput({
                'id': 'inputLocation',
                'placeholder': 'Begin typing the location...',
                'data-set': AutocompleteData.objects
            }),
            'manufacture_date': widgets.DateInput({
                'id': 'inputManufactureDate',
            }),
            'manufacturer': widgets.AutocompleteInput({
                'id': 'inputManufacturer',
                'placeholder': 'Begin typing the manufacturer...',
                'data-set': AutocompleteData.objects
            }),
            'model_number': widgets.TextInput({
                'id': 'inputModelNumber',
                'placeholder': 'Model number'
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
            'serial_number': widgets.TextInput({
                'id': 'inputSerialNumber',
                'placeholder': 'Serial number'
            }),
            'sop_required': widgets.CheckboxInput({
                'id': 'inputSopRequired',
            }),
            'status': widgets.SelectInput({
                'id': 'inputStatus',
                'translator': InventoryItem.get_status_display,
            }),
            'supplier': widgets.AutocompleteInput({
                'id': 'inputSupplier',
                'placeholder': 'Begin typing the supplier...',
                'data-set': AutocompleteData.objects,
            }),
            'tech_id': widgets.TextInput({
                'id': 'inputTechId',
            }),
            'undergraduate': widgets.CheckboxInput({
                'id': 'inputUndergraduate',
            }),
        }
