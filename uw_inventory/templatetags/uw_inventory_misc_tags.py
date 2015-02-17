import re

from django import template

from uw_inventory.models import ItemFile

register = template.Library()


@register.inclusion_tag('uw_inventory/misc/file_icon.html')
def contexual_file_icon(item_file):
    extension = ''
    if item_file.mimetype:
        extension = [key for (key, value) in ItemFile.MIMETYPES.items()
                     if value == item_file.mimetype][0]
    if not extension:
        try:
            extension = re.search('\.(\w+)$', item_file.file_field.name).group(1)
        except:
            raise ValueError('Expected file name to have valid type extension')
    if not extension:
        raise ValueError('Expected file name to have valid type extension')

    file_class = 'file-'
    if extension.lower() in ['xls', 'xlsx']:
        file_class += 'excel'
    elif extension.lower() in ['doc', 'docx']:
        file_class += 'word'
    elif extension.lower() in ['ppt', 'pptx']:
        file_class += 'powerpoint'
    elif extension.lower() == 'pdf':
        file_class += 'pdf'
    elif extension.lower() == 'txt':
        file_class += 'text'
    elif extension.lower() in ['zip', 'gz', '7z', 'bz2']:
        file_class += 'archive'
    elif extension.lower() in ['png', 'jpg', 'jpeg', 'gif']:
        file_class += 'image'
    else:
        file_class += 'file'

    return {'file_class': file_class}
