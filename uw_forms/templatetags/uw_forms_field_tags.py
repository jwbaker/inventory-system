from django import template

register = template.Library()


def _field_handler(field, tag, **kwargs):
    '''
    Fills a context dictionary to pass to the field renderer.

    Positional arguments:
        field -- The Django field object, or None
        tag -- A string representing the caller
                Currently supported: 'edit', 'static' 'field'
    Keyword arguments:
        field_id -- The unique identifier of the field
        field_label -- If field is None, provide the label for the form field
        field_value -- If field is None, provide the value of the field_value
        can_edit -- The Django permissions attribute determining if the user
                    can edit the model this form is based on
    '''
    context = {}
    context['caller'] = tag
    context['field'] = field

    try:
        context['field_value'] = field.value
    except AttributeError:
        context['field_value'] = kwargs.get('field_value', '')

    try:
        context['field_label'] = field.label
    except AttributeError:
        context['field_label'] = kwargs.get('field_label', '') or ''

    try:
        context['field_required'] = field.field.required
    except AttributeError:
        context['field_required'] = False

    context['field_id'] = kwargs.get('field_id', '')
    context['can_edit'] = kwargs.get('can_edit', False)

    return context


@register.inclusion_tag('uw_forms/field_container.html')
def show_editable_field(field, can_edit):
    '''
    Generates a form field with edit, save, and cancel buttons.

    Use for fields in edit forms.

    Positional arguments:
        field -- The Django field object
        can_edit -- The Django permissions attribute determining if the user
                    can edit the model this form is based on
    '''
    return _field_handler(field['field'], 'edit',
                          field_id=field['id'],
                          can_edit=can_edit)


@register.inclusion_tag('uw_forms/field_container.html')
def show_static_field(field):
    '''
    Generates a non-editable form field.

    Positional arguments:
        field -- The Django field object
    '''
    return _field_handler(field['field'], 'static')


@register.inclusion_tag('uw_forms/field_container.html')
def show_excluded_field(field_label, field_value):
    '''
    Generates a special static field widget for excluded fields.

    Positional arguments:
        field_label -- A label for the field
        field_value -- The value of the field
    '''
    return _field_handler(None, 'static',
                          field_label=field_label,
                          field_value=field_value)


@register.inclusion_tag('uw_forms/field_container.html')
def show_field(field):
    '''
    Generates a form control with no extra fluff.

    Use for fields in add forms.

    Positional arguments:
        field --- The Django field object
    '''
    return _field_handler(field['field'], 'field')


@register.inclusion_tag('uw_forms/file_list.html')
def show_files(can_add, can_edit, view_deleted, formset=None):
    '''
    Displays the list of associated files for an InventoryItem

    Positional arguments:
        can_add -- True if the currently logged-in user is allowed to upload
                    files
        can_edit -- True if the currently logged-in user is allowed to edit
                    file properties
        view_deleted -- True if the currently logged-in user is allowed to view
                        'deleted' files
        formset --- The Django set of ItemFile forms associated with the
                        InventoryItem instance
    '''
    if formset:
        return {
            'can_add': can_add,
            'can_edit': can_edit,
            'view_deleted': view_deleted,
            'forms': formset.forms
        }
    else:
        return {
            'can_add': can_add,
            'can_edit': can_edit,
            'view_deleted': view_deleted,
            'forms': None
        }
