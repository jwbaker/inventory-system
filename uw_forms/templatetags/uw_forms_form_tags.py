from django import template

register = template.Library()


def _form_handler(form, form_id, target_view,
                  permissions=None,
                  shown_excluded_fields=None):
    '''
    Packages up a context object for displaying InventoryItem forms

    Positional arguments:
        form -- The Django form object
        permissions -- The Django permissions object of the current user
        creation_date -- A Python datetime.datetime object corresponding to
                         the creation date of the record
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
                    lambda s, r: s+r,
                    field_name_words
                )
        })

        if field.get('Legacy'):
            fields[-1]['legacy'] = True
    context = {
        'form': form,
        'form_id': form_id,
        'target_view': target_view,
        'shown_excluded_fields': shown_excluded_fields,
        'fields': fields,
        'perms': permissions,
    }
    return context


@register.inclusion_tag('uw_forms/add_form.html')
def add_form(form, form_id, target_view):
    '''
    Generates the context data for the InventoryItem add form.

    Positional arguments:
        form -- The Django form object
    '''
    return _form_handler(form, form_id, target_view)
