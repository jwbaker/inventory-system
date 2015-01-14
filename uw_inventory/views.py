from django.contrib import messages
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
    storage = messages.get_messages(request)
    page_messages = []
    for msg in storage:
        if 'page' in msg.extra_tags:
            msg_class = msg.tags.replace(msg.extra_tags, '').replace(' ', '')
            page_messages.append({
                'message': msg.message,
                'class': 'danger' if ('error' in msg_class) else msg_class,
            })

    inventory_item = InventoryItem.objects.get(pk=item_id)
    return render(request, 'uw_inventory/detail.html', {
        'inventory_item': inventory_item,
        'page_messages': page_messages,
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
            messages.error(request, 'Shit broke', extra_tags='page')
        else:
            messages.success(request,
                             'All quiet on the western front',
                             extra_tags='page')

        return HttpResponseRedirect('/list/%s' % new_item.pk)
