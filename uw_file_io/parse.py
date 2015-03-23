import csv
import os
import re
from tempfile import NamedTemporaryFile
from zipfile import BadZipfile, ZipFile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db.models import Q

from uw_inventory.models import (
    AutocompleteData,
    InventoryItem,
    ItemImage,
    ItemFile
)


# Having this data structure makes some things later much easier
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
        'type': 'choice',
        'field_name': 'status',
    },
    'Owner': {
        'type': 'user',
        'field_name': 'owner_id',
    },
    'SOP': {
        'type': 'file',
        'field_name': 'sop_file_id',
    },
    'Picture': {
        'type': 'image',
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
    '''
    Attempts to retrieve a record from the AutocompleteData model tables.

    If it cannot find one, it will create a new dictionary with the relevant
    data, and appends to the provided list

    Positional arguments:
        name -- A name to search for. The search will be case-insensitive, but
                for an exact match only
        kind -- The kind of AutocompleteData to search for
        new_terms_list -- A list of terms that have been created this session.
                            This is an "out" parameter, modified by the method
    '''
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
    '''
    Attempts to retrieve a User record

    If it cannot find one, it will create a new dictionary with the relevant
    data, and appends to the provided list.

    This is more complicated than searching for an Autocomplete term, so it
    may generate a set of results.

    Positional arguments:
        user_value -- A name value to search for
        new_users -- A list of users that have been created this session.
                        This is an "out" parameter, modified by the method
    '''
    matches = User.objects.all()
    if ' ' in user_value:
        for term in user_value.split():
            matches = matches.filter(
                Q(first_name__icontains=term) |
                Q(last_name__icontains=term)
            )
    else:
        matches = matches.filter(
            Q(username__iexact=user_value) |
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


def __parse_inventory_extract(data):
    new_terms = {}
    new_users = {}
    new_items = []
    new_files = []
    new_images = []
    for row in data:
        picture = None
        if row.get('ID', None):
            kwargs = {}

            for (col, val) in row.iteritems():
                store_value = None
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
                    elif field_meta['type'] == 'choice':
                        store_value = InventoryItem.get_status_key(val) or 'SA'
                    elif field_meta['type'] == 'rename':
                        store_value = val or None
                    elif field_meta['type'] == 'file':
                        store_value = val.split('/')[-1]
                        new_files.append(store_value)
                    elif field_meta['type'] == 'image':
                        picture = val.split('/')[-1]
                        new_images.append(val.split('/')[-1])
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
                        'sop_file'
                    ]
                )
            except ValidationError as e:
                print e
                # Back out of all changes so far
                raise ValidationError(
                    '''Failed to insert row {0}. Please look at your file
                                and try again.'''.format(row['ID'])
                )
            else:
                if picture:
                    kwargs['image_id'] = picture
                new_items.append(kwargs)
    response = {
        'status': True,
        'message': 'Import successful',
        'new_items': new_items,
        'new_terms': new_terms,
        'new_users': new_users,
        'new_files': new_files,
        'new_images': new_images,
    }
    return response


def __parse_user_extract(data):
    new_users = []

    for row in data:
        if row['ID']:
            kwargs = {}
            try:
                kwargs = User.objects.get(username=row['Username']).id
            except User.DoesNotExist:
                for (col, val) in row.iteritems():
                    if col in ['First Name', 'Last Name', 'Username']:
                        kwargs[col.lower().replace(' ', '_')] = val
                    else:
                        if val or val.lower == 'yes':
                            kwargs[col.lower().replace(' ', '_')] = True
                        else:
                            kwargs[col.lower().replace(' ', '_')] = False
            except KeyError:
                raise ValidationError(
                    '''Row {0} requires  'Username' field'''.format(row['ID'])
                )
            new_users.append(kwargs)

    return new_users


def parse_extract(file_up, import_type):
    '''
    Parses an extract file into an list of InventoryItems.

    This method does basic validation on non-relational fields.

    Positional arguments:
        file_up -- The Django file object corresponding to the uploaded
                    extract. Accepted file formats are .xls, .xlsx, and .csv

    Returns:
        A dictionary containing lists of the objects that must be created for
        the upload. These lists will be processed by later functions
    '''
    try:
        data = csv.DictReader(file_up)
    except Exception:
        raise ValidationError(
            'Something went wrong. Please look at your file and try again.'
        )

    if import_type == 'InventoryItem':
        return __parse_inventory_extract(data)
    elif import_type == 'User':
        return __parse_user_extract(data)


def parse_zip(file_up):
    new_files = {}
    if file_up is None:
        return new_files

    try:
        with ZipFile(file_up, mode='r') as archive:
            for filename in archive.namelist():
                with archive.open(filename, mode='r') as curr_file:
                    with NamedTemporaryFile(
                            delete=False,
                            dir='media/temp'
                    ) as temp_file:
                        temp_file.write(curr_file.read())
                        new_files[filename] = temp_file.name

    except BadZipfile:
        raise IOError('File was not a *.zip archive.')

    return new_files


def process_terms_transactions(term_list, transactions):
    '''
    Creates Autocomplete terms according to a given list

    Positional arguments:
        term_list -- A list of term instructions to follow. The objects must
                        have the following format:

                        {
                            'action': 'skip' | 'create' | 'rename',
                            'kind': str,
                            'name': name,
                            'type': 'new->new' | 'new->old' (rename only),
                            'replace': str (rename only),
                        }

                        A type of 'new->new' will associate an uncreated term
                        with another uncreated term.

                        A type of 'new->old' will associate an uncreated term
                        with an existing term.

        transactions -- A list of database changes commited over this import.
                        This list is updated in the method to include saved
                        terms, and will later be used as a reference if
                        the import fails and changes must be reverted
    '''
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
    '''
    Creates Users according to a given list

    Positional arguments:
        user_list -- A list of user instructions to follow. The objects must
                        have the following format:

                        {
                            'action': 'skip' | 'create' | 'rename',
                            'kind': str,
                            'name': name,
                            'type': 'new->new' | 'new->old' (rename only),
                            'replace': str (rename only),
                            'data' : {} (create only)
                        }

                        A type of 'new->new' will associate an uncreated user
                        with another uncreated user.

                        A type of 'new->old' will associate an uncreated user
                        with an existing user.

                        The data field contains all of the field data to be
                        filled in with the new user.

        transactions -- A list of database changes commited over this import.
                        This list is updated in the method to include saved
                        terms, and will later be used as a reference if
                        the import fails and changes must be reverted
    '''
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


def __move_tempfile(tempfile_path, file_name):
    os.renames(
        tempfile_path,
        file_name
    )
    os.remove(tempfile_path)


def process_image_transactions(image_list, transactions):
    image_to_index = {}

    for (file_path, temp_file) in image_list.iteritems():
        filename = file_path.split('/')[-1]
        if filename:
            with open(temp_file) as fd:
                temp = ItemImage()
                temp.file_field.save(
                    filename,
                    File(fd),
                    save=True
                )
                image_to_index[filename] = temp.id

            transactions.append('Create ItemImage with id={0}'.format(temp.id))
            __move_tempfile(temp_file, temp.file_field.name)
    return image_to_index


def process_file_transactions(file_list, transactions):
    file_to_index = {}

    for (file_path, temp_file) in file_list.iteritems():
        filename = file_path.split('/')[-1]
        with open(temp_file) as fd:
            temp = ItemFile()
            temp.file_field.save(
                filename,
                File(fd),
                save=True
            )
            file_to_index[filename] = temp.id

        transactions.append('Create ItemFile with id={0}'.format(temp.id))
        __move_tempfile(temp_file, temp.file_field.name)

    return file_to_index


STRING_TO_MODEL = {
    'AutocompleteData': AutocompleteData,
    'InventoryItem': InventoryItem,
    'User': User,
    'ItemFile': ItemFile,
    'ItemImage': ItemImage,
}


def __tokenize_transaction(transaction):
    '''
    Converts a transaction string into a computer-readable dictionary

    Positional arguments:
        transaction -- A transaction string. This string is expected to have
                        the following form:

                        {command} {model} with {argname}={argvalue}...

                        {command} can currently only be 'Create'

                        {model} is defined by the constant STRING_TO_MODEL
    '''
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
    '''
    Processes a list of database transactions and undoes them

    Positional arguments:
        transactions_list -- A list of transaction strings. See the docblock
                                for __tokenize_transaction for more details
    '''
    for transaction in transactions_list:
        tokens = __tokenize_transaction(transaction)

        if tokens['command'] == 'Create':
            Model = STRING_TO_MODEL[tokens['model']]
            item = Model.objects.get(**tokens['args'])

            if tokens['model'] in ['ItemFile', 'ItemImage']:
                os.remove(item.file_field.file.url)
            item.delete()
