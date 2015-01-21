from django import template

register = template.Library()


def _field_handler(field, tag, **kwargs):
    '''
    Fills a context dictionary to pass to the field renderer.

    Positional arguments:
        field -- The Django field object, or None
        tag -- A string representing the caller
                Currently supported: 'edit', 'static', 'field'
    Keyword arguments:
        field_id -- The unique identifier of the field
    '''
    context = {}
    context['caller'] = tag
    context['field'] = field

    try:
        context['field_label'] = field.label
    except:
        context['field_label'] = kwargs.get('field_label', '') or ''

    try:
        context['field_required'] = field.field.required
    except:
        context['field_required'] = False

    context['field_id'] = kwargs.get('field_id', '')

    return context


@register.inclusion_tag('uw_inventory/field_container.html')
def show_editable_field(field, field_id):
    '''
    Generates a form field with edit, save, and cancel buttons. Use for 'edit'

    Positional arguments:
        field -- The Django field object
        field_id -- The unique identifier of the field
    '''
    return _field_handler(field, 'edit',
                          field_id=field_id)


@register.inclusion_tag('uw_inventory/field_container.html')
def show_static_field(field):
    '''
    Generates a non-editable form field.

    Positional arguments:
        field -- The Django field object
    '''
    return _field_handler(field, 'static')


@register.inclusion_tag('uw_inventory/field_container.html')
def show_field(field):
    '''
    Generates a form control. Use for 'add'

    Positional arguments:
        field --- The Django field object
    '''
    return _field_handler(field, 'field')
