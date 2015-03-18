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
        return_string = '''<textarea class="{classes}" maxlength="{length}">
        {value}</textarea>'''
    else:
        return_string = '''<input type="{0}" class="{1}" value="{2}"
        maxlength="{3}" />'''.format(
            field_data.get('type-secondary', '') or field_data['type'] or'text',
            '{classes}',
            '{value}',
            '{length}'
        )

    if field_data.get('type-secondary', '') in ['email', 'password']:
        return_string = '''<div class="input-group item-input">
         <span class="input-group-addon"><i class="fa fa-{0}"></i>
         </span>{1}</div>'''.format(
            FIELD_TYPE_TO_ICON[field_data['type-secondary']],
            return_string.format(
                classes='form-element form-control',
                value=field_data.get('value', ''),
                length=field_data.get('length', '255')
            )
        )
    elif field_data['type'] == 'date':
        return_string = '''<div class="input-group item-input">
         <span class="input-group-addon"><i class="fa fa-{0}"></i>
         </span>{1}</div>'''.format(
            FIELD_TYPE_TO_ICON[field_data['type']],
            return_string.format(
                classes='form-element form-control',
                value=field_data.get('value', ''),
                length=field_data.get('length', '255')
            )
        )
    else:
        return_string = return_string.format(
            classes='form-element form-control item-input',
            value=field_data.get('value', ''),
            length=field_data.get('length', '255')
        )
    return return_string


def __bool_widget_render(field_data):
    return_string = '''<i class="form-element item-input checkbox-2 fa-2x {0}"
    value="{1}"></i>'''.format(
        'checked' if field_data.get('value', False) else '',
        'Yes' if field_data.get('value', False) else 'No'
    )
    return_string += '''<input type="checkbox" class="persist-hidden"
    {0} />'''.format(
        'checked="checked"' if field_data.get('value', False) else ''
    )

    return return_string


def __number_widget_render(field_data):
    input_widget = '''<input type='number' class="{0}" step="{1}" {2}
    />'''.format(
        '{classes}',
        field_data['step'],
        'min="0"' if not field_data['allow-negative'] else ''
    )

    if field_data['type-secondary'] == 'currency':
        return_string = '''<div class="input-group item-input">
        <span class="input-group-addon">$</span>{0}</div>'''

        if field_data['step'] not in ['0.1', '0.01']:
            return_string = return_string.format(
                '{0}<span class="input-group-addon">.00</span>'.format(
                    input_widget.format(classes='form-element form-control')
                )
            )
        else:
            return_string = return_string.format(
                input_widget.format(classes='form-element form-control')
            )
    else:
        return_string = input_widget.format(
                classes='form-element form-control item-input'
            )

    return return_string


@register.simple_tag
def render_custom_widget(field_data):
    if field_data['type'] == 'text':
        widget_string = __text_widget_render(field_data)
    elif field_data['type'] == 'date':
        widget_string = __text_widget_render(field_data)
    elif field_data['type'] == 'bool':
        widget_string = __bool_widget_render(field_data)
    elif field_data['type'] == 'number':
        widget_string = __number_widget_render(field_data)
    else:
        widget_string = ''

    return mark_safe(widget_string)
