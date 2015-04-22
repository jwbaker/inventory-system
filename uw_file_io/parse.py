import csv
from datetime import date
import os
import re
import zipfile

from django.contrib.auth.models import User

from uw_inventory.models import (
    AutocompleteData,
    InventoryItem,
    ItemFile,
    ItemImage
)

FILE_DIRECTORY_RE = re.compile(r'files/\d*/\d*/\d*/?$')
IMAGE_DIRECTORY_RE = re.compile(r'images/\d*/\d*/\d*/?$')


def dict_merge(a, b):
    '''
    Merges the contents of two dictionaries together. Duplicate keys will
    be collapsed into a list of values
    '''
    if not isinstance(a, dict) or not isinstance(b, dict):
        raise TypeError('Expected arguments of type "dict"')
    ret_dict = {}

    for k, v in b.iteritems():
        if k in a:
            if isinstance(a[k], []):
                ret_dict[k] = a[k].append(v)
            else:
                ret_dict[k] = [a[k], v]
        else:
            ret_dict[k] = v

    for k, v in a.iteritems():
        if k not in ret_dict:
            ret_dict[k] = v

    return ret_dict


def __unpack_archive(archive):
    csv_files = []
    files = []

    for name in archive.namelist():
        if name.endswith('.csv'):
            csv_files.append(name)
        elif not name.endswith('/'):
            files.append(name)

        archive.extract(name, path='media/temp')

    return csv_files, files

FILENAME_TO_MODEL = {
    'inventoryitem.csv': InventoryItem,
    'itemimage.csv': ItemImage,
    'itemfile.csv': ItemFile,
}

MODEL_EXCLUDED_FIELDS = {
    'InventoryItem': [
        'supplier_id',
        'manufacturer_id',
        'location_id',
        'owner_id',
        'technician_id',
        'creation_date',
        'to_display',
        'last_modified',
    ],
    'ItemImage': ['mimetype', 'to_display', 'file_field'],
    'ItemFile': ['mimetype', 'to_display', 'file_field'],
}


def __check_existing_term(term, field_name):
    if field_name == 'sop':
        return term
    elif field_name in ['supplier', 'manufacturer', 'location']:
        try:
            existing_term = AutocompleteData.objects.get(
                name=term,
                kind=field_name
            )
            return existing_term.id
        except AutocompleteData.DoesNotExist:
            return term
    elif field_name in ['owner', 'technician']:
        try:
            exact = User.objects.get(username__iexact=term)
            return exact.id
        except User.DoesNotExist:
            candidates = User.objects.filter(username__icontains=term)
            if len(candidates) == 1:
                return candidates[0].id
            return term


def __process_fields(data, fields, files):
    terms = {}
    for field in fields:
        if data[field] == 'None':
            del data[field]
        elif field in ['supplier',
                       'manufacturer',
                       'location',
                       'owner',
                       'technician',
                       'sop',
                       ]:
                if field not in terms:
                    terms[field] = []

                try:
                    term = int(data[field])
                except ValueError:
                    term = __check_existing_term(data[field], field)
                    if term == data[field]:
                        terms[field].append(term)
                    data['{0}_id'.format(field)] = term
                else:
                    data['{0}_id'.format(field)] = term
                del data[field]

        elif field == 'file_field':
            if data[field] not in files:
                raise ValueError(
                    'Expected file "{0}" not found in archive.'.format(
                        data[field]
                    )
                )
        elif field in ['comment', 'itemfile', 'itemimage']:
            del data[field]
        elif not field or not data[field]:
            del data[field]
    return data, terms


def __import_csv(filename, attached_files):
    Model = FILENAME_TO_MODEL[filename]
    model_data = []
    new_terms = {}
    with open(os.path.join('media/temp', filename), 'rb') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            record_data, terms = __process_fields(
                row,
                row.keys(),
                attached_files
            )
            model_data.append(record_data)
            new_terms = dict_merge(new_terms, terms)
    return {
        'status': 'success',
        'model_name': Model.__name__,
        'model_data': model_data,
        'terms': new_terms,
    }


def process_extract(file_up):
    if not file_up:
        raise ValueError

    ret_object = {'model_data': {}, 'new_terms': {}}
    with zipfile.ZipFile(file_up, 'r') as archive:
        csv_files, files = __unpack_archive(archive)

    for f in csv_files:
        f_data = __import_csv(f, files)

        if f_data['status'] == 'fail':
            raise Exception(f_data['errors'])
        ret_object['model_data'][f_data['model_name']] = f_data['model_data']
        ret_object['new_terms'].update(f_data['terms'])
        ret_object['files'] = files

    return ret_object


def process_terms_transactions(term_list):
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
        elif term['action'] == 'rename':
            if term['type'] == 'new->new':
                if term['replace'] in term_to_index:
                    term_to_index[term['name']] = term_to_index[
                        term['replace']
                    ]
                else:  # We haven't processed the parent term yet, so wait
                    term_list.append(term)
            elif term['type'] == 'new->old':
                temp = AutocompleteData.objects.get(
                    kind=term['kind'],
                    name=term['replace']
                )
                term_to_index[term['name']] = temp.id
                term_to_index[term['repalce']] = temp.id

    return term_to_index


def process_user_transactions(user_list):
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
                            'data': {} (create only)
                        }

                        A type of 'new->new' will associate an uncreated user
                        with another uncreated user.

                        A type of 'new->old' will associate an uncreated user
                        with an existing user.

                        The data field contains all of the field data to be
                        filled in with a new user. It will be ignored if the
                        user is associated with another user.
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
        elif user['action'] == 'rename':
            if user['type'] == 'new->new':
                if user['replace'] in user_to_index:
                    user_to_index[user['name']] = user_to_index[
                        user['replace']
                    ]
                else:  # We haven't processed the parent user yet, so wait
                    user_list.append(user)
            elif user['type'] == 'new->old':
                temp = AutocompleteData.objects.get(username=user['replace'])
                user_to_index[user['name']] = temp.id
                user_to_index[user['repalce']] = temp.id

    return user_to_index


def __move_tempfile(file_path, file_type, temp_prefix='media/temp'):
    today = date.today()
    new_path = os.path.join(
            'media',
            '{0}s'.format(file_type),
            today.year,
            '{0:02}'.format(today.month),
            '{0:02}'.format(today.day),
            file_path
        )
    os.renames(
        os.path.join(temp_prefix, file_path),
        new_path
    )
    os.remove(os.path.join(temp_prefix, file_path))
    return new_path


def import_data(model_data, term_to_index, user_to_index, files_list):
    item_list = []

    for data in model_data['InventoryItem']:
        for field in ['location_id', 'manufacturer_id', 'supplier_id']:
            if isinstance(data.get('field', None), str):
                data[field] = term_to_index[data[field]]

        for field in ['owner_id', 'technician_id']:
            if isinstance(data.get('field', None), str):
                data[field] = user_to_index[data[field]]

        item = InventoryItem(**data)
        item.save()
        item_list.append(item)

    for data in model_data['ItemFile'] + model_data['ItemImage']:
        if 'file_field' in data:
            if data['file_field'] not in files_list:
                raise Exception(
                    'Expected file {0} not uploaded'.format(data['file_field'])
                )
            data['file_field'] = __move_tempfile(data['file_field'])

        file_obj = ItemFile(**data)
        file_obj.save()
        item_list.append(file_obj)

    return item_list
