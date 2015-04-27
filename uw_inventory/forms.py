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
        fields = [
            'file_field',
            'description',
            'file_type',
            'remove_file',
            'to_display'
        ]
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

ITEM_FORM_FIELD_LIST = [
        {'name': 'name', 'type': 'text', 'label': 'Name'},
        {
            'name': 'tech_id',
            'type': 'text',
            'legacy': True,
            'label': 'Technician ID'
        },
        {'name': 'description', 'type': 'text', 'label': 'Description'},
        {'name': 'status', 'type': 'choice', 'label': 'Status'},
        {'name': 'location', 'type': 'text', 'label': 'Location'},
        {'name': 'technician', 'type': 'text', 'label': 'Technician'},
        {'name': 'owner', 'type': 'text', 'label': 'Owner'},
        {'name': 'manufacturer', 'type': 'text', 'label': 'Manufacturer'},
        {'name': 'model_number', 'type': 'text', 'label': 'Model number'},
        {'name': 'serial_number', 'type': 'text', 'label': 'Serial number'},
        {
            'name': 'manufacture_date',
            'type': 'date',
            'label': 'Manufacture date'
        },
        {'name': 'supplier', 'type': 'text', 'label': 'Supplier'},
        {
            'name': 'purchase_price',
            'type': 'number',
            'label': 'Purchase price'
        },
        {'name': 'purchase_date', 'type': 'date', 'label': 'Purchase date'},
        {
            'name': 'replacement_cost',
            'type': 'number',
            'label': 'Replacement cost'
        },
        {
            'name': 'replacement_cost_date',
            'type': 'date',
            'label': 'Estimation date'
        },
        {'name': 'csa_required', 'type': 'bool', 'label': 'CSA Required?'},
        {
            'name': 'factory_csa',
            'type': 'bool',
            'label': 'Factory CSA certification?'
        },
        {
            'name': 'csa_special',
            'type': 'bool',
            'label': 'Special CSA inspection required?'
        },
        {
            'name': 'csa_special_date',
            'type': 'date',
            'label': 'Special CSA inspection date'
            },
        {
            'name': 'modified_since_csa',
            'type': 'bool',
            'label': 'Modified since CSA inspection?'
        },
        {
            'name': 'undergraduate',
            'type': 'bool',
            'label': 'Used for undergraduate teaching?',
        },
        {
            'name': 'csa_cost',
            'type': 'number',
            'label': 'CSA Certification cost'
        },
        {'name': 'lifting_device', 'type': 'bool', 'label': 'Lifting device?'},
        {
            'name': 'lifting_device_inspection_date',
            'type': 'date',
            'label': 'Lifting device inspection date'
        },
        {'name': 'notes', 'type': 'text', 'label': 'Notes'},
        {'name': 'sop_required', 'type': 'bool', 'label': 'SOP required?'},
    ]


class ItemForm(forms.ModelForm):
    # This list provides metdata to the field renderer.
    # Most of that logic is field order, but legacy fields are also described
    FIELD_LIST = ITEM_FORM_FIELD_LIST

    class Meta:
        model = InventoryItem
        exclude = [
            'creation_date',
            'last_modified',
            'sop_file',
            'to_display',
            'uuid',
        ]

        labels = {
            data['name']: data['label'] for data in ITEM_FORM_FIELD_LIST
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
                'id': 'inputname',
                'placeholder': 'name',
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
