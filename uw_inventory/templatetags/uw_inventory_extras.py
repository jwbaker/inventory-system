from django import template

from uw_inventory.models import InventoryItem

register = template.Library()


def get_choice_text(arr, choice):
    if choice is None:
        return ''
    list = [t[1] for t in arr if t[0] == choice]
    if len(list) == 1:
        return list[0]
    else:
        raise LookupError(choice + ' was not in the array')


@register.inclusion_tag('uw_inventory/editable_field.html')
def show_editable_field(field_value, field_type, field_label):
    context = {
        'field_value': field_value,
        'field_type': field_type,
        'field_id': 'input' + ''.join(field_label.split()),
        'field_label': field_label,
        'field_name': ('_'.join(field_label.split())).lower()
    }

    if field_type == 'dropdown':
        context['field_value'] = get_choice_text(InventoryItem.STATUS_CHOICES,
                                                 field_value)
        context['field_options'] = InventoryItem.STATUS_CHOICES

    return context
