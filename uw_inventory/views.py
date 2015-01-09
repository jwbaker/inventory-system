from django.shortcuts import render

from uw_inventory.models import InventoryItem


# Create your views here.
def inventory_list(request):
    inventory_list = InventoryItem.objects.all()
    return render(request, 'uw_inventory/list.html', {
        'inventory_list': inventory_list,
    })
