from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

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


# Create your views here.
def inventory_list(request):
    inventory_list = InventoryItem.objects.all()
    return render(request, 'uw_inventory/list.html', {
        'inventory_list': inventory_list,
    })


@csrf_protect
def inventory_detail(request, item_id):
    message_list = _collect_messages(request)

    inventory_item = InventoryItem.objects.get(pk=item_id)
    return render(request, 'uw_inventory/detail.html', {
        'inventory_item': inventory_item,
        'page_messages': message_list['page'],
    })


@csrf_protect
def inventory_save(request, item_id):
    if request.method == 'POST':
        item = InventoryItem.objects.get(pk=item_id)

        for attr in item.EDITABLE_FIELDS:
            if attr in item.NUMERIC_FIELDS and not request.POST[attr]:
                setattr(item, attr, None)
            else:
                setattr(item, attr, request.POST[attr])

        try:
            item.save()
        except Exception as e:
            for err in e.args:
                messages.error(request, err, extra_tags='page')
        else:
            messages.success(request,
                             'All quiet on the western front',
                             extra_tags='page')
    return HttpResponseRedirect('/list/' + item_id)


@csrf_protect
def inventory_add(request):
    message_list = _collect_messages(request)

    return render(request, 'uw_inventory/add.html', {
        'page_messages': message_list['page'],
    })


@csrf_protect
def inventory_new(request):
    if request.method == 'POST':
        args = {}
        dest = None

        for attr in InventoryItem.EDITABLE_FIELDS:
            args[attr] = request.POST[attr] or None

        new_item = InventoryItem(**args)

        try:
            new_item.full_clean()
            new_item.save()
        except Exception as e:
            for err in e.args:
                messages.error(request, err, extra_tags='page')
            dest = '/list/add'
        else:
            messages.success(request,
                             'All quiet on the western front',
                             extra_tags='page')
            dest = '/list/%s' % new_item.pk

        return HttpResponseRedirect(dest)
