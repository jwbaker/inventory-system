import os

from django import template

register = template.Library()


@register.filter
def filename(file_name):
    '''
    Converts a relative file path into a file name

    Positional arguments:
        file_name - The Django File object name
    '''
    return os.path.basename(file_name)
