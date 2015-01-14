from django.core.exceptions import ValidationError
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

        for attr in item.EDITABLE_FIELDS:
            setattr(item, attr, request.POST[attr])

        item.save()
    return HttpResponseRedirect('/list/' + item_id)


@csrf_protect
def inventory_add(request):
    return render(request, 'uw_inventory/add.html')


@csrf_protect
def inventory_new(request):
    if request.method == 'POST':
        args = {}

        for attr in InventoryItem.EDITABLE_FIELDS:
            args[attr] = request.POST[attr]

        new_item = InventoryItem(**args)

        try:
            new_item.full_clean()
            new_item.save()
        except ValidationError:
            err_msg = "Shit broke"
            success = False
        else:
            err_msg = ''
            success = True

        return render(request, 'uw_inventory/detail.html', {
            'inventory_item': new_item,
            'success': success,
            'err_msg': err_msg,
        })
