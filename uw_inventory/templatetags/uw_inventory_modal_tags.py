from django import template

register = template.Library()


@register.inclusion_tag('uw_inventory/modal.html')
def confirm_modal(modal_name):
    context = {
        'buttons': [
            {
                'class': 'default',
                'id': 'confirm%sModalCancel' % modal_name,
                'text': 'Cancel'
            },
            {
                'class': 'danger',
                'id': 'confirm%sModalContinue' % modal_name,
                'position': 'left',
                'text': 'Continue',
            },

        ],
        'id': 'confirm%sModal' % modal_name,
        'title': 'Confirm',
        'body': '''This page has unsaved changes.
                    Are you sure you want to leave?'''
    }
    return context
