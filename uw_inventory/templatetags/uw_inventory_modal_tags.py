from django import template

register = template.Library()


@register.inclusion_tag('uw_inventory/modal.html')
def confirm_modal(modal_name):
    '''
    Generates an unsaved changes confirmation dialogue modal.

    Parameters:
        modal_name -- A unique identifying name for the modal.
                        The id will be generated from this name.
    '''
    context = {
        'buttons': [
            {
                'class': 'default',
                'id': 'confirm{0}ModalCancel'.format(modal_name),
                'text': 'Cancel'
            },
            {
                'class': 'danger',
                'id': 'confirm{0}ModalContinue'.format(modal_name),
                'position': 'left',
                'text': 'Continue',
            },

        ],
        'id': 'confirm{0}Modal'.format(modal_name),
        'title': 'Confirm',
        'body': '''This page has unsaved changes.
                    Are you sure you want to leave?'''
    }
    return context
