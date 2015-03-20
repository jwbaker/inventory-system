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
        return '''
                <textarea
                    class="{classes}"
                    maxlength="{length}">
                        {value}
                </textarea>
                '''.format(
                    classes='form-element form-control item-input',
                    value=field_data.get('value', ''),
                    length=field_data.get('length', '255')
                )
    else:
        input_widget = '''
                        <input
                            class="{classes}"
                            maxlength="{length}"
                            type="{type}"
                            value="{value}" />
                        '''

    if field_data.get('type-secondary', '') in ['email', 'password']:
        return '''
                <div class="input-group item-input">
                    <span class="input-group-addon">
                        <i class="fa-{0}"></i>
                    </span>
                        {1}
                </div>
                '''.format(
                        FIELD_TYPE_TO_ICON[field_data['type-secondary']],
                        input_widget.format(
                            classes='form-element form-control',
                            value=field_data.get('value', ''),
                            length=field_data.get('length', '255'),
                            type=field_data['type-secondary']
                        )
                )
    elif field_data['type'] == 'date':
        return '''
                <div class="input-group item-input">
                    <span class="input-group-addon">
                        <i class="fa-{0}"></i>
                    </span>
                        {1}
                </div>
                '''.format(
                        FIELD_TYPE_TO_ICON[field_data['type-secondary']],
                        input_widget.format(
                            classes='form-element form-control',
                            value=field_data.get('value', ''),
                            length=field_data.get('length', '255'),
                            type=field_data['type']
                        )
                )
    else:
        return input_widget.format(
            classes='form-element form-control item-input',
            value=field_data.get('value', ''),
            length=field_data.get('length', '255'),
            type='text'
        )


def __bool_widget_render(field_data):
    return '''
            <i
                class="form-element item-input checkbox-2 fa-2x {0}"
                value="{1}">
            </i>
            <input
                type="checkbox"
                class="persist-hidden"
                {2} />'''.format(
                    'checked' if field_data.get('value', False) else '',
                    'Yes' if field_data.get('value', False) else 'No',
                    'checked="checked"' if field_data.get('value', False) else ''
            )


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


def __choice_widget_render(field_data):
    if field_data['widget'] == 'multiselect':
        return_string = '''<select class="form-element form-control
        item-input" multiple="multiple">{0}</select>'''
        option_template = '<option value="{0}">{0}</option>'
    elif field_data['widget'] == 'select':
        return_string = '''<select class="form-element form-control item-input">
        {0}</select>'''
        option_template = '<option value="{0}">{0}</option>'
    elif field_data['widget'] in ['checkbox', 'radio']:
        return_string = '<div class="item-input"><form>{0}</form></div>'
        option_template = '''<div><label><input type="{0}" /> {1}
        </label></div>'''.format(
            field_data['widget'],
            '{0}'
        )

    options = ''
    for option in field_data['options']:
        options += option_template.format(option)

    return_string = return_string.format(options)

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
    elif field_data['type'] == 'choice':
        widget_string = __choice_widget_render(field_data)
    else:
        widget_string = ''

    return mark_safe(widget_string)
