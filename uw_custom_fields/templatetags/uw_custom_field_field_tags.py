import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('uw_custom_fields/field_container.html')
def show_custom_fields(field_data_string):
    try:
        field_list = json.loads(field_data_string or '')
    except ValueError:
        field_list = []
    return {'fields': field_list}

FIELD_TYPE_TO_ICON = {
    'email': 'envelope',
    'password': 'key',
    'date': 'calendar',
    'datetime': 'clock-o',
}


def __text_widget_render(field_data):
    if field_data.get('type-secondary', '') == 'textarea':
        return_string = '<textarea class="{classes}">{value}</textarea>'
    else:
        return_string = '<input type="{0}" class="{1}" value="{2}" />'.format(
            field_data.get('type-secondary', '') or field_data['type'] or'text',
            '{classes}',
            '{value}'
        )

    if field_data.get('type-secondary', '') in ['email', 'password']:
        return_string = '''<div class="input-group item-input">
         <span class="input-group-addon"><i class="fa fa-{0}"></i>
         </span>{1}</div>'''.format(
            FIELD_TYPE_TO_ICON[field_data['type-secondary']],
            return_string.format(
                classes='form-element form-control',
                value=field_data.get('value', '')
            )
        )
    elif field_data['type'] == 'date':
        return_string = '''<div class="input-group item-input">
         <span class="input-group-addon"><i class="fa fa-{0}"></i>
         </span>{1}</div>'''.format(
            FIELD_TYPE_TO_ICON[field_data['type']],
            return_string.format(
                classes='form-element form-control',
                value=field_data.get('value', '')
            )
        )
    else:
        return_string = return_string.format(
            classes='form-element form-control item-input',
            value=field_data.get('value', '')
        )
    return return_string


def __date_widget_render(field_data):
    pass


@register.simple_tag
def render_custom_widget(field_data):
    if field_data['type'] == 'text':
        widget_string = __text_widget_render(field_data)
    elif field_data['type'] == 'date':
        widget_string = __text_widget_render(field_data)
    else:
        widget_string = ''

    return mark_safe(widget_string)
