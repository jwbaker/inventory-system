from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from uw_inventory.models import InventoryItem


# Create your views here.
def inventory_list(request):
    inventory_list = InventoryItem.objects.all()
    return render(request, 'uw_inventory/list.html', {
        'inventory_list': inventory_list,
    })


@csrf_protect
def inventory_detail(request, item_id):
    inventory_item = InventoryItem.objects.get(pk=item_id)
    return render(request, 'uw_inventory/detail.html', {
        'inventory_item': inventory_item,
    })


@csrf_protect
def inventory_save(request, item_id):
    if request.method == 'POST':
        item = InventoryItem.objects.get(pk=item_id)
        item.name = request.POST['name']
        item.creation_date = request.POST['creation_date']
        item.description = request.POST['description']
        item.status = request.POST['status']
        item.purchase_price = request.POST['purchase_price']
        item.save()
    return HttpResponseRedirect('/list')
