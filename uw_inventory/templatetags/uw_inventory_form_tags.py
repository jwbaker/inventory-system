from django import template

register = template.Library()


def _form_handler(form, creation_date=None):
    fields = []
    for field in form.FIELD_LIST:
        field_obj = form[field.get('Name')]
        field_name_words = ['input'] + [s.capitalize()
                                        for s in field.get('Name').split('_')]

        fields.append({
            'field': field_obj,
            'id': reduce(
                    lambda s, r: s+r,
                    field_name_words
                )
        })

    context = {'form': form, 'creation_date': creation_date, 'fields': fields}
    return context


@register.inclusion_tag('uw_inventory/forms/edit_form.html')
def edit_form(form, creation_date):
    return _form_handler(form, creation_date)


@register.inclusion_tag('uw_inventory/forms/add_form.html')
def add_form(form):
    return _form_handler(form)
