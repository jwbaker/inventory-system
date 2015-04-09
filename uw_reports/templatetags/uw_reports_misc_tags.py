from django import template
from django.utils.safestring import mark_safe

from uw_inventory.forms import ITEM_FORM_FIELD_LIST

register = template.Library()


@register.filter
def get(dictionary, key):
    '''
    Dynamically retrieves the value of dictionary key
    Useful when we don't know the name of the field at "compile" time
    For example, if we're looping over a list of field names

    Positional arguments:
        dictionary -- The dictionary-like object to lookup in
                        e.g. a Django model instance
        key -- The name of the field to lookup
    '''
    return getattr(dictionary, key, '')


@register.simple_tag()
def visibility_icon(report):
    visibility_class = 'lock'
    visibility_message = 'Only me'
    if not report.owner:
        visibility_class = 'un{0}'.format(visibility_class)
        visibility_message = 'Everyone'

    return mark_safe(
        '''<i class="{0}" title="{1}" data-toggle="tooltip"
            data-placement="left"></i>'''.format(
            visibility_class,
            visibility_message
        )
    )


@register.filter
def to_id(field_name):
    try:
        return [f['name'] for f in ITEM_FORM_FIELD_LIST
                if f['label'] == field_name][0]
    except IndexError:
        return ''
