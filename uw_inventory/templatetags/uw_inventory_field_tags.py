import re

from django import template

from uw_inventory.models import InventoryItem, InventoryItemLocation

register = template.Library()


AUTOCOMPLETE_DATA_CLASSES = {
    'location': InventoryItemLocation,
}


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

    field_label_words = [s.lower().capitalize()
                         for s in field.label.split()]
    context['field_id'] = re.sub(
        r'[^\w]',
        '',
        str('input%s' % ''.join(field_label_words))
    )
    try:
        context['field_label'] = field.label
    except:
        context['field_label'] = kwargs.get('field_label', '') or ''

    try:
        context['field_required'] = field.field.required
    except:
        context['field_required'] = False

    context['field_type'] = kwargs.get('field_type', '') or ''
    context['field_value'] = kwargs.get('field_value', '') or ''

    if context['field_type'] == 'dropdown':
        context['field_value'] = InventoryItem.get_status_display(
            context['field_value']
        )
    elif context['field_type'] == 'boolean':
        context['field_value'] = 'Yes' if context['field_value'] else 'No'
    elif context['field_type'] == 'autocomplete':
        if context['field_value']:
            context['field_value_text'] = AUTOCOMPLETE_DATA_CLASSES[
                field.name
            ].objects.get(id=context['field_value']).name
        else:
            context['field_value_text'] = ''

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
def show_static_field(field):
    '''
    Generates a non-editable form field.

    Positional arguments:
        field -- The Django field object
    '''
    return _field_handler(field, 'static', field_value=field.value)


@register.inclusion_tag('uw_inventory/field_container.html')
def show_field(field, field_type):
    '''
    Generated a form control. Use for 'add'

    Positional arguments:
        field --- The Django field object
        field_type -- Used to choose which input control to render
                  Currently only required for 'currency' types
    '''
    return _field_handler(field, 'field',
                          field_type=field_type)
