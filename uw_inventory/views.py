import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from uw_inventory.forms import ItemForm
from uw_inventory.models import InventoryItem, InventoryItemLocation


def _collect_messages(request):
    '''
    Loops through stored messages and packages them for consumption.

    We need to iterate through in order to mark the message as seen, otherwise
    it will keep displaying on every page.

    This method also converts the 'error' class into the 'danger' class, so
    bootstrap will recognize and render it properly.

    Positional arguments:
        request - The request object passed to the view

    Returns: An array of message objects
    '''
    storage = messages.get_messages(request)
    message_list = []
    for msg in storage:
        msg_class = msg.tags
        message_list.append({
            'message': msg.message,
            'class': 'danger' if ('error' in msg_class) else msg_class,
        })
    return message_list


def inventory_list(request):
    message_list = _collect_messages(request)
    inventory_list = InventoryItem.objects.filter(deleted=False)
    return render(request, 'uw_inventory/list.html', {
        'inventory_list': inventory_list,
        'message_list': message_list,
    })


@csrf_protect
def inventory_detail(request, item_id):
    inventory_item = InventoryItem.objects.get(pk=item_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=inventory_item)

        if form.is_valid():
            form.save()
            messages.success(request,
                             'Item saved successfully')
        else:
            messages.error(request,
                           'Something went wrong. Check below for errors')

    else:
        form = ItemForm(instance=inventory_item)

    message_list = _collect_messages(request)
    return render(request, 'uw_inventory/detail.html', {
        'inventory_item': inventory_item,
        'form': form,
        'page_messages': message_list,
        'creation_date': inventory_item.creation_date,
    })


@csrf_protect
def inventory_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            messages.success(request,
                             'Inventory item saved successfully')
            new_item = form.save()
            return HttpResponseRedirect('/list/%s' % new_item.pk)
        else:
            print form.errors
            messages.error(request,
                           'Something went wrong. Check below for errors')
    else:
        form = ItemForm()
    message_list = _collect_messages(request)
    return render(request, 'uw_inventory/add.html', {
        'form': form,
        'page_messages': message_list,
    })


def inventory_copy(request, item_id):
    item = InventoryItem.objects.get(pk=item_id)
    item.pk = None
    try:
        item.save()
    except:
        messages.error(request,
                       'Something went wrong')
    else:
        messages.success(request,
                         'Duplication was successful')

    return HttpResponseRedirect('/list/%s' % item.pk)


def inventory_delete(request, item_id):
    item = InventoryItem.objects.get(pk=item_id)
    item.deleted = True
    try:
        item.save()
    except:
        messages.error(request,
                       'Something went wrong')
        dest = '/list/%s' % item_id
    else:
        messages.success(request,
                         'Deleted')
        dest = '/list/'
    return HttpResponseRedirect(dest)


def locations_list(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        location_results = InventoryItemLocation.objects.filter(
            name__icontains=query
        )
        data = []
        for location in location_results:
            location_json = {}
            location_json['id'] = location.id
            location_json['label'] = location.name
            location_json['value'] = location.name
            data.append(location_json)
        response = json.dumps(data)
    else:
        response = 'fail'
    mimetype = 'application/json'
    return HttpResponse(response, mimetype)
