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
    image_files = []
    file_files = []

    for name in archive.namelist():
        if name.endswith('.csv'):
            csv_files.append(name)
        elif 'files/' in name and FILE_DIRECTORY_RE.search(name) is None:
            file_files.append(name)
        elif 'images/' in name and IMAGE_DIRECTORY_RE.search(name) is None:
            image_files.append(name)

        archive.extract(name, path='media/temp')

    return csv_files, image_files, file_files

FILENAME_TO_MODEL = {
    'inventory_item.csv': InventoryItem,
    'item_image.csv': ItemImage,
    'item_file.csv': ItemFile,
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
    new_terms = {}
    for field in fields:
        if field in data.keys():
            if field in ['supplier_id',
                         'manufacturer_id',
                         'location_id',
                         'owner_id',
                         'technician_id'
                         ]:
                try:
                    data[field] = int(data[field])
                except ValueError:
                    new_terms[data[field]] = {'kind': data[field][:-3]}
            elif field == 'file_field':
                if data[field] not in files:
                    raise ValueError(
                        'Expected file "{0}" not found in archive.'.format(
                            data[field]
                        )
                    )
    return data, new_terms


def __import_csv(filename, attached_files):
    Model = FILENAME_TO_MODEL[filename]
    model_data = []
    with open(os.path.join('media/temp', filename), 'rb') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            record = Model(**row)
            try:
                record.full_clean(
                    exclude=MODEL_EXCLUDED_FIELDS[Model.__name__]
                )
            except ValidationError as e:
                return {'status': 'fail', 'errors': e.message_dict}
            else:
                record_data, new_terms = __process_excluded_fields(
                    row,
                    MODEL_EXCLUDED_FIELDS[Model.__name__],
                    attached_files
                )
                model_data.append(record_data)

    return {
        'status': 'success',
        'model_name': Model.__name__,
        'payload': model_data,
        'new_terms': new_terms,
    }


def process_extract(file_up):
    if not file_up:
        raise ValueError

    ret_object = {'model_data': {}, 'new_terms': []}
    with zipfile.ZipFile(file_up, 'r') as archive:
        csv_files, image_files, file_files = __unpack_archive(archive)

    for f in csv_files:
        f_data = __import_csv(f)

        if f_data['status'] == 'fail':
            raise Exception(f_data['errors'])
        ret_object['model_data'][f_data['model_name']] = f_data['payload']
        ret_object['new_terms'].append(f_data['new_terms'])

    return ret_object
