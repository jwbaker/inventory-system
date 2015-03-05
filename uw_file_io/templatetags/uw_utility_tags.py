from django import template

register = template.Library()


@register.filter
def get(dict, key):
    '''
    Performs a dynamic dictionary lookup

    Django's template system by default only allows us to access dictionary
    properties that are known, but in this app we need to lookup fields based
    on a variable.

    This tag acts exactly like a regular dictionary lookup.
    This means that it will raise an error if the key does not exist, or if it
    if passed something that it not a dictionary

    Positional arguments:
        dict -- A Python dictionary
        key -- The key in dict to lookup
    '''
    return dict.get(key)
