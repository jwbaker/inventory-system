import csv
import os
import re
import zipfile

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


def __import_csv(filename):
    Model = FILENAME_TO_MODEL[filename]
    with open(os.path.join('media/temp', filename), 'rb') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            record = Model(**row)
            try:
                record.save()  # Django is smart enough to update when needed
            except Exception as e:
                return {'status': 'fail', 'errors': str(e)}

    return {'status': 'success'}


def process_extract(file_up):
    if not file_up:
        raise ValueError

    ret_object = {}
    with zipfile.ZipFile(file_up, 'r') as archive:
        csv_files, image_files, file_files = __unpack_archive(archive)

    for f in csv_files:
        f_status = __import_csv(f)

        if f_status['status'] == 'fail':
            raise Exception(f_status['errors'])

    return ret_object
