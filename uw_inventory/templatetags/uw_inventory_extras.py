from django import template

from uw_inventory.models import InventoryItem

register = template.Library()


def get_choice_text(arr, choice):
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


@register.inclusion_tag('uw_inventory/editable_field.html')
def show_editable_field(field_value, field_type, field_label):
    """Generates a form field with edit, save, and cancel buttons.

    Positional arguments:
    field_value -- The current value of the field
    field_type -- Used to choose which input control to render
                  Currently supported: 'text', 'currency', 'dropdown',
                  'textarea'
    field_label -- A unique identifier for the field. Expected to be the
                    Title Cased name of the model variable
    """
    context = {
        'field_value': field_value,
        'field_type': field_type,
        'field_id': 'input' + ''.join(field_label.split()),
        'field_label': field_label,
        'field_name': ('_'.join(field_label.split())).lower()
    }

    if field_type == 'dropdown':
        if field_value:
            context['field_value'] = get_choice_text(
                InventoryItem.STATUS_CHOICES,
                field_value
            )
        context['field_options'] = InventoryItem.STATUS_CHOICES

    return context
