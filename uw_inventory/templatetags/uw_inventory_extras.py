from django import template

from uw_inventory.models import InventoryItem

register = template.Library()


def _get_choice_text(arr, choice):
    '''
    Performs a lookup in an array of 2-tuples.

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
    '''
    Fills a context dictionary to pass to the field renderer.

    Positional arguments:
        field -- The Django field object, or None
        tag -- A string representing the caller
                Currently supported: 'edit', 'static', 'field'
    Keyword arguments:
        field_label -- Label to display next to the field. For consistency,
                        this should be the sentence-cased name of the field
        field_value -- The current value of the field
    '''
    context = {}
    context['caller'] = tag
    context['field'] = field

    try:
        context['field_id'] = str('input%s' % ''.join(field.label.split()))
        context['field_label'] = field.label
        context['field_required'] = field.field.required
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
    '''
    Generates a form field with edit, save, and cancel buttons. Use for 'edit'

    Positional arguments:
        field -- The Django field object
        field_value -- The current value of the field
        field_type -- Used to choose which input control to render
                  Currently only required for 'currency' types
    '''
    return _field_handler(field, 'edit',
                          field_value=field_value,
                          field_type=field_type)


@register.inclusion_tag('uw_inventory/field_container.html')
def show_static_field(field_label, field_value):
    '''
    Generates a non-editable form field.

    Positional arguments:
        field_label -- Label to display next to the field. For consistency,
                        this should be the sentence-cased name of the field
        field_value -- The current value of the field
    '''
    return _field_handler(None, 'static',
                          field_label=field_label,
                          field_value=field_value)


@register.inclusion_tag('uw_inventory/field_container.html')
def show_field(field, field_type):
    '''
    Generated a form control. Use for 'add'

    Positional arguments:
        field --- The Django field object
        field_type -- Used to choose which input control to render
                  Currently only required for 'currency' types
    '''
    return _field_handler(field, 'field', field_type=field_type)
