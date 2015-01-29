from django import template

register = template.Library()


@register.inclusion_tag('uw_inventory/notes_list.html')
def show_notes(note_set):
    return {
        'note_set': note_set,
    }
