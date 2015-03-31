from django import template

register = template.Library()


@register.filter
def get(dictionary, key):
    '''
    Dynamically retrieves the value of dictionary key
    Useful when we don't know the name of the field at "compile" time
    For example, if we're looping over a list of field names

    Positional arguments:
        dictionary -- The dictionary-like object to lookup in
                        e.g. a Django model instance
        key -- The name of the field to lookup
    '''
    return getattr(dictionary, key, '')
