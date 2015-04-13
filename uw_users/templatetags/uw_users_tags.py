from django import template

register = template.Library()


@register.inclusion_tag('uw_users/context_menu.html')
def user_context_menu(user):
    '''
    Renders a dropdown menu with user-specific commands

    Positional arguments:
        user -- The Django user object for the currently logged-in user
    '''
    context = {
        'user': user,
        'perms': [],
    }

    if user.is_staff:
        context['perms'].append('admin')

    if user.has_perm('change_user'):
        context['perms'].append('user_list')

    return context


@register.filter
def spacify(val):
    return val.replace(' ', '%20').replace('/', '%2F')
