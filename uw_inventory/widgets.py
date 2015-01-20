from django import forms
from django.utils.safestring import mark_safe


class AutocompleteInput(forms.Widget):
    def render(self, name, value, attrs=None):
        try:
            data_source = self.attrs['data-set']
            value_label = data_source.get(pk=value).name
        except:
            value_label = ''

        try:
            widget_id = self.attrs['id']
        except:
            widget_id = None

        try:
            widget_class = self.attrs['class']
        except:
            widget_class = None

        try:
            widget_placeholder = self.attrs['placeholder']
        except:
            widget_placeholder = None

        input_ctl = u'''<input id="{0}"
                               class="{1}"
                               placeholder="{2}"
                               value="{3}" />
                        <input id="{0}"
                               class="{1} hidden autocomplete-hidden"
                               value="{4}"
                               name="{5}" />'''.format(
                                 widget_id,
                                 widget_class,
                                 widget_placeholder,
                                 value_label,
                                 value if value else '',
                                 name
                               )
        return mark_safe(input_ctl)


class CheckboxInput(forms.Widget):

    def render(self, name, value, attrs=None):
        try:
            widget_id = self.attrs['id']
        except:
            widget_id = None

        try:
            widget_class = self.attrs['class']
        except:
            widget_class = ''
        widget_class += ' checkbox fa fa-2x'
        widget_class += ' {0}'.format(
            'fa-check-square-o' if value else 'fa-square-o'
        )

        input_ctl = '''<input type="checkbox" id="{0}" name="{1}"
                        class="hidden" {2} />'''.format(
            widget_id,
            name,
            'checked="checked"' if value else ''
        )

        return mark_safe(
            u'<i class="{0}" id="{1}" name="{2}" value="{3}">{4}</i>'.format(
                widget_class,
                widget_id,
                name,
                value,
                input_ctl
            )
        )


# We need this class because Django's default date widget is a text box
class DateInput(forms.DateInput):
    input_type = 'date'
