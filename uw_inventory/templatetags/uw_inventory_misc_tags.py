from django import template

from uw_inventory.models import ItemFile

register = template.Library()


@register.inclusion_tag('uw_inventory/misc/file_icon.html')
def contexual_file_icon(item_file):
    extension = ''
    try:
        extension = ItemFile.MIMETYPE_TO_EXTENSION[item_file.mimetype]
    except KeyError:
        extension = item_file.file_field.name.split('.')[-1]

    file_class = 'file-'
    if extension in ['xls', 'xlsx']:
        file_class += 'excel'
    elif extension in ['doc', 'docx']:
        file_class += 'word'
    elif extension in ['ppt', 'pptx']:
        file_class += 'powerpoint'
    elif extension == 'pdf':
        file_class += 'pdf'
    elif extension == 'txt':
        file_class += 'text'
    elif extension in ['zip', 'gz', '7z', 'bz2']:
        file_class += 'archive'
    elif extension in ['png', 'jpg', 'jpeg', 'gif']:
        file_class += 'image'
    else:
        file_class += 'file'

    return {'file_class': file_class}
