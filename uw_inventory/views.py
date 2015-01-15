from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from uw_inventory.forms import ItemForm
from uw_inventory.models import InventoryItem


def _collect_messages(request):
    storage = messages.get_messages(request)
    message_list = {'page': []}
    for msg in storage:
        #if 'page' in msg.extra_tags:
        msg_class = msg.tags.replace(msg.extra_tags, '').replace(' ', '')
        message_list['page'].append({
            'message': msg.message,
            'class': 'danger' if ('error' in msg_class) else msg_class,
        })
    return message_list


def inventory_list(request):
    message_list = _collect_messages(request)
    inventory_list = InventoryItem.objects.all()
    return render(request, 'uw_inventory/list.html', {
        'inventory_list': inventory_list,
        'message_list': message_list['page'],
    })


@csrf_protect
def inventory_detail(request, item_id):
    inventory_item = InventoryItem.objects.get(pk=item_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=inventory_item)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Item saved successfully',
                             extra_tags='page')
        else:
            messages.error(request,
                           'Something went wrong. Check below for errors',
                           extra_tags='page')
        return HttpResponseRedirect('/list/' + item_id)
    else:
        message_list = _collect_messages(request)
        form = ItemForm(instance=inventory_item)

        return render(request, 'uw_inventory/detail.html', {
            'inventory_item': inventory_item,
            'form': form,
            'form_data': form.instance,
            'page_messages': message_list['page'],
        })


@csrf_protect
def inventory_add(request):
    message_list = _collect_messages(request)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            new_item = form.save()
            messages.success(request,
                             'Item saved successfully',
                             extra_tags='page')
            dest = '/list/%s' % new_item.id
        else:
            messages.error(request,
                           'Something went wrong. Check below for errors',
                           extra_tags='page')
            dest = '/list/add'
        return HttpResponseRedirect(dest)
    else:
        form = ItemForm()
        return render(request, 'uw_inventory/add.html', {
            'form': form,
            'page_messages': message_list['page'],
        })
