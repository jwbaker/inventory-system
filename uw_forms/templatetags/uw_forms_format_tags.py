import os

from django import template

register = template.Library()


@register.filter
def filename(file):
    return os.path.basename(file)
