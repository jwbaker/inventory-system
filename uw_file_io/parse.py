import zipfile


def __unpack_archive(archive):
    csv_files = []
    image_files = []
    file_files = []

    for name in archive.namelist():
        print name

    return csv_files, image_files, file_files


def process_extract(file_up):
    if not file_up:
        raise ValueError

    ret_object = {}
    with zipfile.ZipFile(file_up, 'r') as archive:
        csv_files, image_files, file_files = __unpack_archive(archive)

    return ret_object
