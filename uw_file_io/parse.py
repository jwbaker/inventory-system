import re

import pyexcel
import pyexcel.ext.xlsx

from django.core.exceptions import ValidationError

from uw_inventory.models import AutocompleteData, InventoryItem


IMPORT_FIELD_DATA = {
    'ID': {
        'type': 'skip',
    },
    'Attachements': {
        'type': 'skip',
    },
    'Location': {
        'type': 'autocomplete',
        'autocomplete_kind': 'location',
        'field_name': 'location_id',
    },
    'Manufacturer': {
        'type': 'autocomplete',
        'autocomplete_kind': 'manufacturer',
        'field_name': 'manufacturer_id',
    },
    'Supplier': {
        'type': 'autocomplete',
        'autocomplete_kind': 'supplier',
        'field_name': 'supplier_id',
    },
    'Technician': {
        'type': 'skip',
    },
    'Status': {
        'type': 'skip',
    },
    'Owner': {
        'type': 'skip',
    },
    'SOP': {
        'type': 'skip',
    },
    'Picture': {
        'type': 'skip',
    },
    'Lifting_Device_Inspected_By': {
        'type': 'skip',
    },
    'CSA_Required': {
        'type': 'boolean',
        'field_name': 'csa_required',
    },
    'Factory_CSA': {
        'type': 'boolean',
        'field_name': 'factory_csa',
    },
    'CSA_Special': {
        'type': 'boolean',
        'field_name': 'csa_special',
    },
    'Modified_Since_CSA': {
        'type': 'boolean',
        'field_name': 'modified_since_csa',
    },
    'Undergraduate': {
        'type': 'boolean',
        'field_name': 'undergraduate',
    },
    'Manufacture_Date': {
        'type': 'date',
        'field_name': 'manufacture_date',
    },
    'Purchase_Date': {
        'type': 'date',
        'field_name': 'purchase_date',
    },
    'Replacement_Cost_Date': {
        'type': 'date',
        'field_name': 'replacement_cost_date',
    },
    'CSA_Special_Date': {
        'type': 'date',
        'field_name': 'csa_special_date',
    },
    'Purchase_Price': {
        'type': 'currency',
        'field_name': 'purchase_price',
    },
    'Replacement_Cost': {
        'type': 'currency',
        'field_name': 'replacement_cost',
    },
    'CSA_Cost': {
        'type': 'currency',
        'field_name': 'csa_cost',
    },
    'Apparatus': {
        'type': 'rename',
        'field_name': 'name',
    },
    'Model': {
        'type': 'rename',
        'field_name': 'model_number',
    },
    'Serial': {
        'type': 'rename',
        'field_name': 'serial_number',
    },
    'Tech_ID': {
        'type': 'rename',
        'field_name': 'tech_id',
    },
    'Notes': {
        'type': 'rename',
        'field_name': 'notes',
    },
    'MME_ID': {
        'type': 'skip',
    },
    'Description': {
        'type': 'rename',
        'field_name': 'description',
    },
}


def __get_autocomplete_term_or_create(name, kind, new_terms_list):
    try:
        var = AutocompleteData.objects.get(
            name__iexact=name,
            kind=kind
        )
    except AutocompleteData.DoesNotExist:
        var = AutocompleteData(name=name, kind=kind)
        if kind not in new_terms_list:
            new_terms_list[kind] = []

        # This is another uniqueness test - we don't want to add the same item
        # to our new_terms list twice.

        # This function call essentially boils down to a long if-chain, so that
        # array_contains = list[0] == var.name or list[1] == var.name or ...

        # If any one element in the array fails the test, the whole thing will
        # be false.
        array_contains = reduce(
            lambda b, i: b or i.name == var.name,
            new_terms_list[kind],
            False
        )

        if not array_contains:
            new_terms_list[kind].append(var)
    return var


def parse_file(file_up):
    extension = file_up.name.split('.')[1]
    try:
        sheet = pyexcel.load_from_memory(
            extension,
            file_up.read(),
            name_columns_by_row=0
        )
    except NotImplementedError:
        return {
            'status': False,
            'message': '''Invalid file type {0}. Please upload one of: xls, xlsx, csv.
            '''.format(extension),
            'destination': 'uw_file_io.views.file_import',
        }

    else:
        data = sheet.to_records()
        new_terms = {}
        new_items = []
        for row in data:
            if row['ID']:
                kwargs = {}

                for (col, val) in row.iteritems():
                    try:
                        field_meta = IMPORT_FIELD_DATA[col]
                        if field_meta['type'] == 'skip':
                            continue
                        elif field_meta['type'] == 'autocomplete':
                            if val:
                                temp = __get_autocomplete_term_or_create(
                                    val,
                                    field_meta['autocomplete_kind'],
                                    new_terms
                                )
                                store_value = temp.id or temp.name
                        elif field_meta['type'] == 'boolean':
                            store_value = (
                                True if val == 'yes' else False
                            )
                        elif field_meta['type'] == 'date':
                            if val:
                                date_components = val.split('-')
                                assembled_date = '{0}-{1}-{2}'.format(
                                    date_components[2],
                                    date_components[1],
                                    date_components[0]
                                )
                                store_value = assembled_date
                            else:
                                store_value = None
                        elif field_meta['type'] == 'currency':
                            currencyRE = re.match(r'^\$(\d+)\.\d{2}$', val)
                            if currencyRE:
                                store_value = int(currencyRE.group(1))
                            else:
                                store_value = 0
                        elif field_meta['type'] == 'rename':
                            store_value = val or None

                        kwargs[field_meta['field_name']] = store_value
                    except KeyError:
                        pass

                item = InventoryItem(**kwargs)
                try:
                    item.full_clean(
                        exclude=[
                            'uuid',
                            'location',
                            'manufacturer',
                            'supplier'
                        ]
                    )
                except ValidationError as e:
                    print e
                    # Back out of all changes so far
                    return {
                        'status': False,
                        'message': '''Failed to insert row {0}. Please look at your file
                                    and try again.'''.format(row['ID']),
                    }
                else:
                    new_items.append(kwargs)
        response = {
            'status': True,
            'message': 'Import successful',
            'new_items': new_items,
            'new_terms': new_terms,
        }
        return response


def process_terms_transactions(term_list):
    term_to_index = {}

    while len(term_list) > 0:
        term = term_list.pop(0)

        if term['action'] == 'skip':
            continue
        elif term['action'] == 'create':
            temp = AutocompleteData(
                kind=term['kind'],
                name=term['name']
            )
            temp.save()

            term_to_index[term['name']] = temp.id
        elif term['action'] == 'rename':
            if term['type'] == 'new->new':  # Assoc new with new
                if term['replace'] in term_to_index:
                    term_to_index[term['name']] = term_to_index[
                        term['replace']
                    ]
                else:
                    term_list.append(term)
            elif term['type'] == 'new->old':  # Assoc new with existing
                temp = AutocompleteData.objects.get(
                    kind=term['kind'],
                    name=term['replace']
                )
                term_to_index[term['name']] = temp.id
                term_to_index[term['replace']] = temp.id
            elif term['type'] == 'old->new':
                temp = AutocompleteData.objects.get(
                    kind=term['kind'],
                    name=term['name']
                )
                temp.name = term['replace']
                temp.save()
                term_to_index[term['replace']] = temp.id
                term_to_index[term['name']] = temp.id

    return term_to_index
