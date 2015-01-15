from django import template

from uw_inventory.models import InventoryItem

register = template.Library()


def _get_choice_text(arr, choice):
    '''Performs a lookup in an array of 2-tuples.

    Positional arguments:
    arr -- Array of two-element 2-tuples
    choice -- A key to search in the tuples for

    Returns: the second element of the first matching tuple.
             If it doesn't exist, returns an empty string.
    '''
    if choice is None:
        return ''
    list = [t[1] for t in arr if t[0] == choice]
    if len(list) == 1:
        return list[0]
    else:
        return ''


def _field_handler(field, tag, **kwargs):
    context = {}
    context['caller'] = tag
    context['field'] = field

    try:
        context['field_id'] = str('input%s' % ''.join(field.label.split()))
        context['field_label'] = field.label
    except:
        context['field_label'] = kwargs.get('field_label', '') or ''

    context['field_type'] = kwargs.get('field_type', '') or ''
    context['field_value'] = kwargs.get('field_value', '') or ''

    if(context['field_type'] == 'dropdown'):
        context['field_value'] = _get_choice_text(
            InventoryItem.STATUS_CHOICES,
            context['field_value']
        )
    return context


@register.inclusion_tag('uw_inventory/field_container.html')
def show_editable_field(field, field_value, field_type):
    """Generates a form field with edit, save, and cancel buttons.

    Positional arguments:
    field -- The Django field object
    field_value -- The current value of the field
    field_type -- Used to choose which input control to render
                  Currently supported: 'text', 'currency', 'dropdown',
                  'textarea'
    """
    return _field_handler(field, 'edit',
                          field_value=field_value,
                          field_type=field_type)


@register.inclusion_tag('uw_inventory/field_container.html')
def show_static_field(field_label, field_value):
    return _field_handler(None, 'static',
                          field_label=field_label,
                          field_value=field_value)


@register.inclusion_tag('uw_inventory/field_container.html')
def show_field(field, field_type):
    return _field_handler(field, 'field', field_type=field_type)
