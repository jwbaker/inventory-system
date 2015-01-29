from django import template

register = template.Library()


@register.inclusion_tag('uw_users/context_menu.html')
def user_context_menu(user):
    context = {
        'user': user,
        'perms': [],
    }

    if user.is_staff:
        context['perms'].append('admin')

    if user.has_perm('change_user'):
        context['perms'].append('user_list')

    return context
