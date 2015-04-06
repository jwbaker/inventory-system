from django import template
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

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


@register.filter
def admin_url(instance):
    return reverse(
        'admin:uw_inventory_{0}_history'.format(
            type(instance).__name__.lower()
        ),
        args=(instance.id,)
    )


@register.filter
def in_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False
    else:
        return group in user.groups.all() or user.is_superuser


@register.inclusion_tag('uw_inventory/misc/admin_context_menu.html')
def inventory_admin_context_menu():
    return
