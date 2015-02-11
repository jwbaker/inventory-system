from django import template

register = template.Library()


@register.inclusion_tag('uw_inventory/notes_list.html')
def show_notes(note_set, can_add):
    '''
    Shows the notes associated with an InventoryItem

    Positional arguments:
        note_set: The list of Note objects associated with the InventoryItem
                    instance
        can_add: True if the currently logged-in user is allowed to add notes
    '''
    return {
        'note_set': note_set,
        'can_add': can_add
    }
