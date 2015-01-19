from django import forms
from django.utils.safestring import mark_safe


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
