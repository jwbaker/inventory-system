from django import template

register = template.Library()


@register.inclusion_tag('uw_inventory/notes_list.html')
def show_notes(note_set):
    '''
    Shows the notes associated with an InventoryItem

    Positional arguments:
        note_set: The list of Note objects associated with the InventoryItem
                    instance
    '''
    return {
        'note_set': note_set,
    }
