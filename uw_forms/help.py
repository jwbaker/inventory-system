from django.utils.safestring import mark_safe

AUTOCOMPLETE_HELP = '''Typing in this field will bring up a list of similar
                        terms which have been used in other inventory items. If
                        you cannot find the term you want in this list,
                        clicking on the 'Add {0}' link will allow you to add a
                        new one.'''
AUTOCOMPLETE_USER_HELP = '''Typing in this field will bring up a list of users
                            in the system. If you cannot find the user you
                            want, clicking on the 'Add user' link will allow
                            you to add a new one. This user will not have the
                            ability to access this system; if you want them to
                            have that ability, please contact an administrator'''

DEPRECATED_HELP = '''This field has been deprecated. Changes to its value are
                    not allowed.'''

DATE_HELP = 'Please enter dates in dd/mm/yyyy format'

FIELD_HELP_TEXT = {
    'Location': AUTOCOMPLETE_HELP.format('location'),
    'Supplier': AUTOCOMPLETE_HELP.format('supplier'),
    'Manufacturer': AUTOCOMPLETE_HELP.format('manufacturer'),
    'Owner': AUTOCOMPLETE_USER_HELP,
    'Technician': AUTOCOMPLETE_USER_HELP,
    'Technician ID': DEPRECATED_HELP,
    'Manufacture date': DATE_HELP,
    'Purchase date': DATE_HELP,
    'Estimation date': DATE_HELP,
    'Special CSA inspection date': DATE_HELP,
    'Lifting device inspection date': DATE_HELP,
}


def dispatch(field_name):
    return mark_safe(FIELD_HELP_TEXT.get(field_name, ''))
