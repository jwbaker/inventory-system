import os

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def filename(file_name):
    '''
    Converts a relative file path into a file name

    Positional arguments:
        file_name - The Django File object name
    '''
    return os.path.basename(file_name)


@register.filter
def prefix(html_value, index=0):
    return mark_safe(html_value.replace('__prefix__', str(index)))
