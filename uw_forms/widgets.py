from datetime import datetime

from django import forms
from django.utils.safestring import mark_safe


def _common_attributes_handler(attrs):
    '''
    Packages a context object containing attributes common to all widgets.

    Positional arguments:
        attrs -- The attrs dictionary of the widget instance
    '''
    context = {}
    context['id'] = attrs.get('id', '')
    context['class'] = 'form-element '
    context['class'] += attrs.get('class', '')
    context['class'] += ' '
    return context


def _render_static_label(field_id, field_value):
    '''
    Formats the HTML string for the uneditable field value label.

    Positional arguments:
        field_id -- The unique identifier of the field
        field_value -- The current value of the field
    '''
    return u'''<p class="form-control-static" id="{0}">
                  {1}
              </p>'''.format(field_id, field_value or '')


def _render_default_value(field_id, field_value):
    '''
    Formats an HTML string to contain the default value of the field.

    We use this to check if a change has actually occurred, so we need to store
    the original value of the field somewhere immutable.

    Positional arguments:
        field_id -- The unique identifier of the field
        field_value -- The current value of the field
    '''
    return u'''<span class="persist-hidden default-value" for="{0}">
                {1}</span>'''.format(field_id, field_value or '')


class AutocompleteInput(forms.Widget):
    def __init__(self, attrs=None):
        if attrs:
            context = _common_attributes_handler(attrs)
            context['class'] += 'form-control item-input '
            context['placeholder'] = attrs.get('placeholder', '')
            context['data-set'] = attrs.get('data-set', None)
        else:
            context = None

        return super(AutocompleteInput, self).__init__(attrs=context)

    def render(self, name, value, attrs=None):
        widget_id = self.attrs.get('id', '')
        widget_class = self.attrs.get('class', '')
        widget_placeholder = self.attrs.get('placeholder', '')

        try:
            data_source = self.attrs['data-set']
            value_label = data_source.get(pk=value).get_name_display()
        except:
            value_label = ''

        render_str = _render_static_label(widget_id, value_label)

        render_str += u'''<input id="{0}"
                               class="{1}"
                               placeholder="{2}"
                               value="{3}" />
                        <a class="small autocomplete-add-term hidden"
                           data-set="{5}">
                            Add option
                        </a>
                        <input id="{0}"
                               class="{1} hidden persist-hidden"
                               value="{4}"
                               name="{5}" />'''.format(
                                 widget_id,
                                 widget_class,
                                 widget_placeholder,
                                 value_label,
                                 value if value else '',
                                 name
                               )
        render_str += _render_default_value(widget_id, value_label)
        return mark_safe(render_str)


class CheckboxInput(forms.Widget):
    def __init__(self, attrs=None):
        if attrs:
            context = _common_attributes_handler(attrs)
            context['class'] += 'item-input '
            context['placeholder'] = attrs.get('placeholder', 0)
        else:
            context = None

        return super(CheckboxInput, self).__init__(attrs=context)

    def render(self, name, value, attrs=None):
        widget_id = self.attrs.get('id', '')
        widget_class = self.attrs.get('class', '')
        widget_class += ' checkbox-2 fa fa-2x'
        widget_class += ' {0}'.format(
            'checked' if value else 'unchecked'
        )
        display_value = 'Yes' if value else 'No'

        render_str = _render_static_label(widget_id, display_value)

        render_str += '''<i class="{0}" id="{1}" name="{2}" value="{3}">
                        </i>'''.format(
                            widget_class,
                            widget_id,
                            name,
                            display_value
                        )
        render_str += u'''<input type="checkbox" id="{0}" name="{1}"
                        class="persist-hidden" {2} />'''.format(
            widget_id,
            name,
            'checked="checked"' if value else ''
        )

        render_str += _render_default_value(widget_id, display_value)

        return mark_safe(render_str)


class CurrencyInput(forms.NumberInput):
    def __init__(self, attrs=None):
        if attrs:
            context = _common_attributes_handler(attrs)
            context['class'] += 'form-control '
            context['placeholder'] = attrs.get('placeholder', 0)

        else:
            context = None

        return super(CurrencyInput, self).__init__(attrs=context)

    def render(self, name, value, attrs=None):
        render_str = _render_static_label(self.attrs.get('id', ''), value)
        render_str += u'''<div class="input-group item-input">
                            <span class="input-group-addon">$</span>'''

        render_str += super(CurrencyInput, self).render(
            name,
            value,
            attrs
        )

        render_str += u'''<span class="input-group-addon">.00</span>
                        </div>'''
        render_str += _render_default_value(self.attrs.get('id', ''), value)

        return mark_safe(render_str)


class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, attrs=None):
        if attrs:
            context = _common_attributes_handler(attrs)
            context['class'] += 'form-control item-input '
            context['placeholder'] = attrs.get('placeholder', 0)
        else:
            context = None

        return super(DateInput, self).__init__(attrs=context)

    def render(self, name, value, attrs=None):
        try:
            display_value = value.strftime('%b. %d, %Y') if value else ''
        except AttributeError:
            display_value = datetime.strptime(
                                str(value),
                                '%Y-%m-%d'
                            ).strftime('%b. %d, %Y')
        render_str = _render_static_label(
            self.attrs.get('id', ''),
            display_value
        )
        render_str += super(DateInput, self).render(name, value, attrs)
        render_str += _render_default_value(
            self.attrs.get('id', ''),
            display_value
        )
        return mark_safe(render_str)


class SelectInput(forms.Select):
    def __init__(self, attrs=None):
        if attrs:
            context = _common_attributes_handler(attrs)
            context['class'] += 'form-control item-input '
            context['translator'] = attrs.get('translator', None)
        else:
            context = None

        return super(SelectInput, self).__init__(attrs=context)

    def render(self, name, value, attrs=None):
        display_value = self.attrs['translator'](value)
        render_str = _render_static_label(
            self.attrs.get('id', ''),
            display_value
        )
        render_str += super(SelectInput, self).render(name, value, attrs)
        render_str += _render_default_value(
            self.attrs.get('id', ''),
            display_value
        )
        return mark_safe(render_str)


class TextareaInput(forms.Textarea):
    def __init__(self, attrs=None):
        if attrs:
            context = _common_attributes_handler(attrs)
            context['class'] += 'form-control item-input '
            context['placeholder'] = attrs.get('placeholder', '')
            context['style'] = 'resize:vertical '
            context['style'] += attrs.get('style', '')
            context['rows'] = '5'
        else:
            context = None

        return super(TextareaInput, self).__init__(attrs=context)

    def render(self, name, value, attrs=None):
        render_str = _render_static_label(self.attrs.get('id', ''), value)
        render_str += super(TextareaInput, self).render(name, value, attrs)
        render_str += _render_default_value(self.attrs.get('id', ''), value)
        return mark_safe(render_str)


class TextInput(forms.TextInput):
    def __init__(self, attrs=None):
        if attrs:
            context = _common_attributes_handler(attrs)
            context['class'] += 'form-control item-input '
            context['placeholder'] = attrs.get('placeholder', '')
        else:
            context = None

        return super(TextInput, self).__init__(attrs=context)

    def render(self, name, value, attrs=None):
        render_str = _render_static_label(self.attrs.get('id', ''), value)
        render_str += super(TextInput, self).render(name, value, attrs)
        render_str += _render_default_value(self.attrs.get('id', ''), value)
        return mark_safe(render_str)
