from datetime import datetime

from django import forms
from django.utils.safestring import mark_safe


def _common_attributes_handler(attrs):
    context = {}
    context['id'] = attrs.get('id', '')
    context['class'] = 'form-element '
    context['class'] += attrs.get('class', '')
    return context


def _render_static_label(field_id, field_value):
    return u'''<p class="form-control-static" id="{0}">
                  {1}
              </p>'''.format(field_id, field_value or '')


def _render_default_value(field_id, field_value):
    return u'''<span class="field-hidden default-value" for="{0}">
                {1}</span>'''.format(field_id, field_value or '')


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
            value_label = data_source.get(pk=value).name
        except:
            value_label = ''

        render_str = _render_static_label(widget_id, value_label)

        render_str += u'''<input id="{0}"
                               class="{1}"
                               placeholder="{2}"
                               value="{3}" />
                        <a class="small autocomplete-add-term" data-set="{5}">
                            Add option
                        </a>
                        <input id="{0}"
                               class="{1} hidden field-hidden"
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
        widget_class += ' checkbox fa fa-2x'
        widget_class += ' {0}'.format(
            'fa-check-square-o' if value else 'fa-square-o'
        )
        display_value = 'Yes' if value else 'No'

        render_str = _render_static_label(widget_id, display_value)

        render_str += '''<i class="{0}" id="{1}" name="{2}" value="{3}">
                        </i>'''.format(
                            widget_class,
                            widget_id,
                            name,
                            value
                        )
        render_str += u'''<input type="checkbox" id="{0}" name="{1}"
                        class="field-hidden" {2} />'''.format(
            widget_id,
            name,
            'checked="checked"' if value else ''
        )

        render_str += _render_default_value(widget_id, display_value)

        return mark_safe(render_str)


# We need this class because Django's default date widget is a text box
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
