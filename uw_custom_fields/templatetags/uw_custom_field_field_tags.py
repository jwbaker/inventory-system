import json

from django import template

register = template.Library()


@register.inclusion_tag('uw_custom_fields/field_container.html')
def show_custom_fields(field_data_string):
    try:
        field_list = json.loads(field_data_string or '')
    except ValueError:
        field_list = []
    return {'fields': field_list}
