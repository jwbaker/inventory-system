import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from django_cas.decorators import permission_required

from uw_inventory.forms import ItemForm
from uw_inventory.models import (
    AutocompleteData,
    InventoryItem
)


def _collect_messages(request):
    '''
    Loops through stored messages and packages them for consumption.

    We need to iterate through in order to mark the message as seen, otherwise
    it will keep displaying on every page.

    This method also converts the 'error' class into the 'danger' class, so
    bootstrap will recognize and render it properly.

    Positional arguments:
        request - The request object passed to the view
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


def _json_builder_user(user):
    '''
    Converts a user into a JSON object for autocomplete consumption

    Positional arguments:
        user -- the Django User object
    '''
    if user.first_name and user.last_name:
        label = '{0} {1} ({2})'.format(
            user.first_name,
            user.last_name,
            user.username
        )
    else:
        label = user.username
    return {
        'id': user.id,
        'label': label,
        'value': label,
    }


def _json_builder_autocomplete(obj):
    '''
    Converts a term record into a JSON object for autocomplete consumption

    Positional arguments:
        obj -- the AutocompleteData object
    '''
    return {
        'id': obj.id,
        'label': obj.name,
        'value': obj.name,
    }


@permission_required('uw_inventory.view_item')
def inventory_list(request):
    message_list = _collect_messages(request)
    inventory_list = InventoryItem.objects.filter(deleted=False)
    return render(request, 'uw_inventory/list.html', {
        'inventory_list': inventory_list,
        'page_messages': message_list,
    })


@csrf_protect
@permission_required('uw_inventory.view_item')
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
        'shown_excluded_fields': [
            {'label': 'Creation date', 'value': inventory_item.creation_date}
        ]
    })


@csrf_protect
@permission_required('uw_inventory.add_inventoryitem')
def inventory_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            messages.success(request,
                             'Inventory item saved successfully')
            new_item = form.save()
            return HttpResponseRedirect('/list/%s' % new_item.pk)
        else:
            messages.error(request,
                           'Something went wrong. Check below for errors')
    else:
        form = ItemForm()

    message_list = _collect_messages(request)
    return render(request, 'uw_inventory/add.html', {
        'form': form,
        'page_messages': message_list,
    })


@permission_required('uw_inventory.add_inventoryitem')
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


@permission_required('uw_inventory.change_inventoryitem')
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


@permission_required('uw_inventory.change_inventoryitem')
def autocomplete_list(request, source):
    if request.is_ajax():
        query = request.GET.get('term', '')
        data = []

        if source in ['technician', 'owner']:
            result_set = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
            json_builder = _json_builder_user
        else:
            result_set = AutocompleteData.objects.filter(
                kind=source,
                name__icontains=query
            )
            json_builder = _json_builder_autocomplete

        for result in result_set:
            data.append(json_builder(result))
        response = json.dumps(data)
    else:
        response = 'fail'
    mimetype = 'application/json'
    return HttpResponse(response, mimetype)


@csrf_protect
@permission_required('uw_inventory.add_autocompletedata')
def autocomplete_new(request):
    response = {}
    if request.is_ajax() and request.method == 'POST':
        name = request.POST['termName']
        data_set = request.POST['dataSet']
        try:
            if data_set == 'user':
                request_obj = User(
                    username=name,
                    first_name=request.POST['termFirstName'],
                    last_name=request.POST['termLastName']
                )
            else:
                request_obj = AutocompleteData(
                    name=name,
                    kind=data_set
                )
            request_obj.save()
        except IntegrityError:
            error = 'The {0} "{1}" already exists.'.format(data_set, name)
            response = json.dumps({'error': error})
        else:
            response = json.dumps({})
    return HttpResponse(response, 'application/json')
