from django import forms
from django.contrib.auth.models import User

from uw_forms import widgets
from uw_inventory.models import (
    AutocompleteData,
    InventoryItem,
    ItemFile,
    ItemImage,
    Comment,
)


class FileForm(forms.ModelForm):
    class Meta:
        model = ItemFile
        fields = ['file_field', 'description', 'file_type', 'to_display']
        widgets = {
            'description': forms.Textarea({
                'id': 'inputDescription',
                'class': 'form-control form-element',
                'placeholder': 'Description',
                'rows': 2,
            }),
            'file_type': forms.Select({
                'id': 'inputFieldType',
                'class': 'form-control form-element',
            }),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['file_field', 'description', 'to_display']
        widgets = {
            'description': forms.Textarea({
                'id': 'inputDescription',
                'class': 'form-control form-element',
                'placeholder': 'Description',
                'rows': 2,
            }),
        }


class ItemForm(forms.ModelForm):
    # This list provides metdata to the field renderer.
    # Most of that logic is field order, but legacy fields are also described
    FIELD_LIST = [
        {'Name': 'name', 'type': 'text'},
        {'Name': 'tech_id', 'type': 'text', 'Legacy': True},
        {'Name': 'description', 'type': 'text'},
        {'Name': 'status', 'type': 'choice'},
        {'Name': 'location', 'type': 'text'},
        {'Name': 'technician', 'type': 'text'},
        {'Name': 'owner', 'type': 'text'},
        {'Name': 'manufacturer', 'type': 'text'},
        {'Name': 'model_number', 'type': 'text'},
        {'Name': 'serial_number', 'type': 'text'},
        {'Name': 'manufacture_date', 'type': 'date'},
        {'Name': 'supplier', 'type': 'text'},
        {'Name': 'purchase_price', 'type': 'number'},
        {'Name': 'purchase_date', 'type': 'date'},
        {'Name': 'replacement_cost', 'type': 'number'},
        {'Name': 'replacement_cost_date', 'type': 'date'},
        {'Name': 'csa_required', 'type': 'bool'},
        {'Name': 'factory_csa', 'type': 'bool'},
        {'Name': 'csa_special', 'type': 'bool'},
        {'Name': 'csa_special_date', 'type': 'date'},
        {'Name': 'modified_since_csa', 'type': 'bool'},
        {'Name': 'undergraduate', 'type': 'bool'},
        {'Name': 'csa_cost', 'type': 'number'},
        {'Name': 'lifting_device', 'type': 'bool'},
        {'Name': 'lifting_device_inspection_date', 'type': 'date'},
        {'Name': 'notes', 'type': 'text'},
        {'Name': 'sop_required', 'type': 'bool'},
    ]

    class Meta:
        model = InventoryItem
        exclude = [
            'creation_date',
            'last_modified',
            'sop_file',
            'to_display',
            'uuid',
        ]

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
            'custom_field_data': widgets.TextareaInput({
                'id': 'inputCustomFields',
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
            'notes': widgets.TextareaInput({
                'id': 'inputNotes',
                'placeholder': 'Notes',
                'rows': 5,
            }),
            'owner': widgets.AutocompleteInput({
                'id': 'inputOwner',
                'placeholder': 'Begin typing the name or UWID...',
                'data-set': User.objects,
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
                'translator': InventoryItem.get_status,
            }),
            'supplier': widgets.AutocompleteInput({
                'id': 'inputSupplier',
                'placeholder': 'Begin typing the supplier...',
                'data-set': AutocompleteData.objects,
            }),
            'tech_id': widgets.TextInput({
                'id': 'inputTechId',
            }),
            'technician': widgets.AutocompleteInput({
                'id': 'inputTechnician',
                'placeholder': 'Begin typing the name or UWID...',
                'data-set': User.objects,
            }),
            'undergraduate': widgets.CheckboxInput({
                'id': 'inputUndergraduate',
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'creation_date', 'author']

        widgets = {
            'body': forms.Textarea({
                'id': 'inputBody',
                'class': 'form-control',
                'placeholder': 'Comment'
            }),
        }
