import re

import pyexcel
import pyexcel.ext.xlsx

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

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
        'type': 'user',
        'field_name': 'technician_id',
    },
    'Status': {
        'type': 'skip',
    },
    'Owner': {
        'type': 'user',
        'field_name': 'owner_id',
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


def __get_user_id_or_create(user_value, new_users):
    matches = User.objects.filter(
        Q(username=user_value) |
        Q(first_name__icontains=user_value) |
        Q(last_name__icontains=user_value)
    )

    if len(matches) == 0:
        new_users[user_value] = None
    elif len(matches) == 1:
        return matches[0].id
    else:
        new_users[user_value] = matches

    return user_value


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

    data = sheet.to_records()
    new_terms = {}
    new_users = {}
    new_items = []
    for row in data:
        if row['ID']:
            kwargs = {}

            for (col, val) in row.iteritems():
                try:
                    field_meta = IMPORT_FIELD_DATA[col]
                    if field_meta['type'] == 'skip':
                        continue
                    elif field_meta['type'] == 'user':
                        if val:
                            temp = __get_user_id_or_create(
                                val,
                                new_users
                            )
                            store_value = temp or val
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
                        'supplier',
                        'owner',
                        'technician',
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
            'new_users': new_users,
        }
        return response


def process_terms_transactions(term_list, transactions):
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
            transactions.append(
                'Create AutocompleteData with id={0}'.format(temp.id)
            )
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

    return term_to_index


def process_user_transactions(user_list, transactions):
    user_to_index = {}

    while len(user_list) > 0:
        user = user_list.pop(0)

        if user['action'] == 'skip':
            continue
        elif user['action'] == 'create':
            temp = User(**user['data'])
            temp.save()
            user_to_index[user['name']] = temp.id

            transactions.append(
                'Create User with id={0}'.format(temp.id)
            )
        elif user['action'] == 'rename':
            if user['type'] == 'new->new':
                if user['replace'] in user_to_index:
                    user_to_index[user['name']] = user_to_index[
                        user['replace']
                    ]
                else:
                    user_list.append(user)
            elif user['type'] == 'new->old':
                temp = User.objects.get(username=user['replace'])
                user_to_index[user['name']] = temp.id
                user_to_index[user['replace']] = temp.id

    return user_to_index


STRING_TO_MODEL = {
    'AutocompleteData': AutocompleteData,
    'InventoryItem': InventoryItem,
    'User': User,
}


def __tokenize_transaction(transaction):
    retObject = {}

    retObject['command'] = transaction.split(None, 1)[0]
    retObject['model'] = transaction.split(None, 2)[1]
    retObject['args'] = {}

    for token in transaction.split(None, 2)[2].split():
        if token == 'with':
            continue
        else:
            args = token.split('=')
            retObject['args'][args[0]] = args[1]

    return retObject


def reverse_transactions(transactions_list):
    for transaction in transactions_list:
        tokens = __tokenize_transaction(transaction)

        if tokens['command'] == 'Create':
            Model = STRING_TO_MODEL[tokens['model']]
            item = Model.objects.get(**tokens['args'])
            item.delete()
