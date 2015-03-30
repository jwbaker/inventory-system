from django import template

register = template.Library()


@register.filter
def get(dictionary, key):
    return getattr(dictionary, key, '')
