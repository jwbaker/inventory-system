import json
import os

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

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
            if parse_response['new_terms']:
                request.session['NewTerms'] = parse_response['new_terms']
        return redirect(parse_response['destination'])

    message_list = _collect_messages(request)
    return render(request, 'uw_file_io/import.html', {
        'form': ImportForm(),
        'page_messages': message_list,
    })


def __process_import(request, item_list, term_list):
    term_to_index = process_terms_transactions(term_list)
    new_items = []

    for item_args in item_list:
        if isinstance(item_args['location_id'], unicode):
            item_args['location_id'] = term_to_index[item_args['location_id']]
        if isinstance(item_args['manufacturer_id'], unicode):
            item_args['location_id'] = term_to_index[
                item_args['manufacturer_id']
            ]

        item = InventoryItem(**item_args)
        item.save()
        new_items.append(item)

    return render(request, 'uw_file_io/import_done.html', {
        'item_list': new_items,
    })


@csrf_protect
def add_terms(request):
    if request.method == 'POST':
        item_list = request.session['IntermediateItems']
        new_terms = json.loads(request.POST['termHierarchy'])

        del request.session['IntermediateItems']
        del request.session['NewTerms']

        return __process_import(request, item_list, new_terms)
    return render(request, 'uw_file_io/new_terms.html', {
        'new_terms': request.session['NewTerms'],
        'old_terms': {
            'location': [t.name for t in
                         AutocompleteData.objects.filter(kind='location')],
            'manufacturer': [t.name for t in
                             AutocompleteData.objects.filter(
                                 kind='manufacturer'
                             )],
        }
    })
