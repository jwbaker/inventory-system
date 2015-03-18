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


def __text_widget_render(field_data):
    if field_data['type-secondary'] == 'textarea':
        widget_string = '<textarea class="{classes}">{value}</textarea>'
    else:
        widget_string = '<input type="{0}" class="{1}" value="{2}" />'.format(
            field_data['type-secondary'] or 'text',
            '{classes}',
            '{value}'
        )

    if field_data['type-secondary'] in ['email', 'password']:
        widget_string = '''<div class="input-group item-input">
         <span class="input-group-addon"><i class="fa fa-{0}"></i>
         </span>{1}</div>'''.format(
            'envelope' if field_data['type-secondary'] == 'email' else 'key',
            widget_string.format(
                classes='form-element form-control',
                value=field_data.get('value', '')
            )
        )
    else:
        widget_string = widget_string.format(
            classes='form-element form-control item-input',
            value=field_data.get('value', '')
        )
    return widget_string


@register.simple_tag
def render_custom_widget(field_data):
    if field_data['type'] == 'text':
        widget_string = __text_widget_render(field_data)

    return mark_safe(widget_string)
