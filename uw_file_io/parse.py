import csv
import os
import re
import zipfile

from django.core.exceptions import ValidationError

from uw_inventory.models import InventoryItem, ItemFile, ItemImage

FILE_DIRECTORY_RE = re.compile(r'files/\d*/\d*/\d*/?$')
IMAGE_DIRECTORY_RE = re.compile(r'images/\d*/\d*/\d*/?$')


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


def __process_excluded_fields(data, fields, files):
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
                terms[field].append(data[field])
                del data[field]
                data['{0}_id'.format(field)] = terms[field][-1]
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
    with open(os.path.join('media/temp', filename), 'rb') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            record_data, terms = __process_excluded_fields(
                row,
                row.keys(),
                attached_files
            )
            model_data.append(record_data)

    return {
        'status': 'success',
        'model_name': Model.__name__,
        'model_data': model_data,
        'terms': terms,
    }


def process_extract(file_up):
    if not file_up:
        raise ValueError

    ret_object = {'model_data': {}, 'terms': []}
    with zipfile.ZipFile(file_up, 'r') as archive:
        csv_files, files = __unpack_archive(archive)

    for f in csv_files:
        f_data = __import_csv(f, files)

        if f_data['status'] == 'fail':
            raise Exception(f_data['errors'])
        ret_object['model_data'][f_data['model_name']] = f_data['model_data']
        ret_object['terms'].append(f_data['terms'])

    return ret_object
