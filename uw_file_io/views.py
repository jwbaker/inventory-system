import json
import os

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from django_cas.decorators import permission_required

from uw_file_io.forms import ImportForm
from uw_file_io.parse import process_terms_transactions, parse_file
from uw_inventory.models import (
    AutocompleteData,
    InventoryItem,
    ItemFile
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


def file_download(request, file_id):
    if request.method == 'GET':
        file = ItemFile.objects.get(id=file_id).file_field
        response = HttpResponse(file)
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            os.path.basename(file.name)
        )

        return response


def file_view(request, file_name):
    if request.method == 'GET':
        file_obj = ItemFile.objects.get(file_field=file_name)
        with open(file_name, 'r') as file:
            response = HttpResponse(
                file.read(),
                content_type=file_obj.mimetype
            )
            response['Content-Disposition'] = 'inline; filename="{0}"'.format(
                os.path.basename(file.name)
            )
            return response
        file.closed


@csrf_protect
@permission_required('uw_inventory.add_inventoryitem')
def file_import(request):
    if request.method == 'POST':
        parse_response = parse_file(request.FILES['file_up'])
        if not parse_response['status']:
            messages.error(
                request,
                parse_response['message']
            )
        else:
            request.session['IntermediateItems'] = parse_response['new_items']
            request.session['NewTerms'] = parse_response['new_terms']

        if 'NewTerms' in request.session:
            destination = 'uw_file_io.views.add_terms'
        else:
            destination = 'uw_file_io.views.finish_import'

        return redirect(destination)

    message_list = _collect_messages(request)
    return render(request, 'uw_file_io/import.html', {
        'form': ImportForm(),
        'page_messages': message_list,
    })


@csrf_protect
def add_terms(request):
    if request.method == 'POST':
        request.session['NewTerms'] = json.loads(request.POST['termHierarchy'])

        return redirect('uw_file_io.views.finish_import')

    return render(request, 'uw_file_io/new_terms.html', {
        'new_terms': request.session['NewTerms'],
        'old_terms': {
            'location': [t.name for t in
                         AutocompleteData.objects.filter(kind='location')],
            'manufacturer': [t.name for t in
                             AutocompleteData.objects.filter(
                                 kind='manufacturer'
                             )],
            'supplier': [t.name for t in
                         AutocompleteData.objects.filter(
                             kind='supplier'
                         )],
        }
    })


def finish_import(request):
    item_list = request.session['IntermediateItems']
    term_list = request.session['NewTerms']

    term_to_index = process_terms_transactions(term_list)
    new_items = []

    for item_args in item_list:
        if (
                'location_id' in item_args and
                item_args['location_id'] and
                isinstance(item_args['location_id'], unicode)
        ):
            item_args['location_id'] = term_to_index[item_args['location_id']]
        if (
                'manufacturer_id' in item_args and
                item_args['manufacturer_id'] and
                isinstance(item_args['manufacturer_id'], unicode)
        ):
            item_args['manufacturer_id'] = term_to_index[
                item_args['manufacturer_id']
            ]
        if (
                'supplier_id' in item_args and
                item_args['supplier_id'] and
                isinstance(item_args['supplier_id'], unicode)
        ):
            item_args['supplier_id'] = term_to_index[
                item_args['supplier_id']
            ]

        item = InventoryItem(**item_args)
        item.save()
        new_items.append(item)

    del request.session['IntermediateItems']
    del request.session['NewTerms']

    return render(request, 'uw_file_io/import_done.html', {
        'item_list': new_items,
    })
