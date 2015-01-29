from django import template

register = template.Library()


def _form_handler(form, form_id, target_view,
                  can_edit=False,
                  shown_excluded_fields=None):
    '''
    Packages up a context object for displaying forms

    Positional arguments:
        form -- The Django form object
        form_id -- A unique identifier for the form
        target_view -- A string representing the form target view
                        Passed to URL template tag
        can_edit -- The Django permissions attribute determining if the user
                    can edit the model this form is based on. Default False
        shown_excluded_fields -- A list of dictionaries representing otherwise-
                                 excluded fields to display with the form.
                                 Format: [{'label', 'value'}]
    '''
    fields = []
    for field in form.FIELD_LIST:
        field_obj = form[field.get('Name')]
        field_name_words = ['input'] + [s.capitalize()
                                        for s in field.get('Name').split('_')]

        fields.append({
            'field': field_obj,
            # reduce function accumulates the array into a single string
            'id': reduce(
                lambda s, r: s + r,
                field_name_words
            )
        })

        if field.get('Legacy'):
            # Negative list slicing is SO COOL
            fields[-1]['legacy'] = True

    try:
        instance = getattr(form.instance, form.INSTANCE_MEMBER)
    except AttributeError:
        instance = form.instance.id

    context = {
        'form': form,
        'form_id': form_id,
        'target_view': target_view,
        'shown_excluded_fields': shown_excluded_fields,
        'fields': fields,
        'can_edit': can_edit,
        'instance': instance
    }
    return context


@register.inclusion_tag('uw_forms/add_form.html')
def add_form(form, form_id, target_view=None):
    '''
    Generates the context data for a model add form.

    Positional arguments:
        form -- The Django form object
        form_id -- A unique identifier for the form
        target_view -- A string representing the form target view
                        Passed to URL template tag
    '''
    return _form_handler(form, form_id, target_view)


@register.inclusion_tag('uw_forms/edit_form.html')
def edit_form(form, form_id, target_view, can_edit,
              shown_excluded_fields=None):
    '''
    Generates the context data for a model display page/edit form.

    Positional arguments:
        form -- The Django form object
        form_id -- A unique identifier for the form
        target_view -- A string representing the form target view
                        Passed to URL template tag
        can_edit -- The Django permissions attribute determining if the user
                    can edit the model this form is based on. Default False
        shown_excluded_fields -- A list of dictionaries representing otherwise-
                                 excluded fields to display with the form.
                                 Format: [{'label', 'value'}]
    '''
    return _form_handler(
        form,
        form_id,
        target_view,
        can_edit,
        shown_excluded_fields
    )
