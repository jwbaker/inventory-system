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


def _field_handler(field_label, tag, **kwargs):
    context = {}
    context['field_label'] = field_label
    context['caller'] = tag

    context['field_value'] = kwargs.get('field_value', '') or ''
    context['field_type'] = kwargs.get('field_type', '') or ''

    context['field_name'] = ('_'.join(context['field_label'].split())).lower()
    context['field_id'] = 'input' + ''.join(context['field_label'].split())
    context['field_hidden'] = context['caller'] == 'edit'

    if context['field_type'] == 'dropdown':
        if context['field_value']:
            context['field_value'] = _get_choice_text(
                InventoryItem.STATUS_CHOICES,
                context['field_value']
            )
        context['field_options'] = InventoryItem.STATUS_CHOICES

    return context


@register.inclusion_tag('uw_inventory/field_container.html')
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
    return _field_handler(field_label, 'edit',
                          field_value=field_value,
                          field_type=field_type)


@register.inclusion_tag('uw_inventory/field_container.html')
def show_static_field(field_value, field_label):
    return _field_handler(field_label, 'static', field_value=field_value)


@register.inclusion_tag('uw_inventory/field_container.html')
def show_field(field_type, field_label):
    return _field_handler(field_label, 'field', field_type=field_type)
