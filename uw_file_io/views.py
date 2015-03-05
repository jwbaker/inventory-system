import json
import os

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from django_cas.decorators import permission_required

from uw_file_io.forms import ImportForm
from uw_file_io.parse import (
    process_terms_transactions,
    process_user_transactions,
    parse_file,
    reverse_transactions
)
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
            request.session['NewUsers'] = parse_response['new_users']

        if 'NewTerms' in request.session and request.session['NewTerms']:
            destination = 'uw_file_io.views.add_terms'
        elif 'NewUsers' in request.session and request.session['NewUsers']:
            return redirect('uw_file_io.views.add_users')
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

        if 'NewUsers' in request.session and request.session['NewUsers']:
            return redirect('uw_file_io.views.add_users')
        else:
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


@csrf_protect
def add_users(request):
    if request.method == 'POST':
        request.session['NewUsers'] = json.loads(request.POST['userHierarchy'])
        return redirect('uw_file_io.views.finish_import')
    return render(request, 'uw_file_io/new_users.html', {
        'new_users': request.session['NewUsers'],
        'old_users': User.objects.all(),
    })


def finish_import(request):
    item_list = request.session['IntermediateItems']
    term_list = request.session['NewTerms']
    user_list = request.session['NewUsers']
    transactions = []

    term_to_index = process_terms_transactions(term_list, transactions)
    user_to_index = process_user_transactions(user_list, transactions)
    new_items = []

    for item_args in item_list:
        for field in ['location_id', 'manufacturer_id', 'supplier_id']:
            if (
                    field in item_args and
                    item_args[field] and
                    isinstance(item_args[field], unicode)
            ):
                item_args[field] = term_to_index[item_args[field]]

        for field in ['technician_id', 'owner_id']:
            if (
                    field in item_args and
                    item_args[field] and
                    isinstance(item_args[field], unicode)
            ):
                item_args[field] = user_to_index[item_args[field]]

        item = InventoryItem(**item_args)
        try:
            item.save()
        except ValidationError:
            messages.error(
                request,
                'There was a problem with your file.'
            )
            reverse_transactions(transactions)
            return redirect('uw_file_io.views.file_import')
        else:
            transactions.append(
                'Create InventoryItem with id={0}'.format(item.id)
            )
            new_items.append(item)

    del request.session['IntermediateItems']
    del request.session['NewTerms']
    del request.session['NewUsers']

    return render(request, 'uw_file_io/import_done.html', {
        'item_list': new_items,
    })
