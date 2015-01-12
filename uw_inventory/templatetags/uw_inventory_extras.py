from django import template

from uw_inventory.models import InventoryItem

register = template.Library()


@register.inclusion_tag('uw_inventory/editable_field.html')
def show_editable_field(field_value, field_type, field_label):
    context = {
        'field_value': field_value,
        'field_type': field_type,
        'field_id': 'input' + ''.join(field_label.split()),
        'field_label': field_label,
    }

    if field_type == 'dropdown':
        context['field_options'] = InventoryItem.STATUS_CHOICES

    return context
