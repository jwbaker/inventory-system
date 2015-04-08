import csv
import json
import os
import zipfile

from django.conf import settings
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
    process_image_transactions,
    process_file_transactions,
    parse_extract,
    parse_zip,
    reverse_transactions,
)
from uw_inventory.models import (
    AutocompleteData,
    InventoryItem,
    ItemFile,
    ItemImage
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
        # Clear these session tokens on every file upload
        # This will (hopefully) prevent unexpected behaviour if the user
        # does some silliness
        request.session.pop('ImportType', None)
        request.session.pop('IntermediateItems', None)
        request.session.pop('NewTerms', None)
        request.session.pop('NewUsers', None)
        request.session.pop('NewFiles', None)
        request.session.pop('NewImages', None)

        if request.POST['model'] == 'II':
            request.session['ImportType'] = 'InventoryItem'
            try:
                parse_response = parse_extract(
                    request.FILES['file_up'],
                    'InventoryItem'
                )
            except (TypeError, ValidationError) as e:
                messages.error(
                    request,
                    str(e[0])
                )
                return redirect('uw_file_io.views.file_import')
            else:
                request.session['IntermediateItems'] = parse_response[
                    'new_items'
                ]
                request.session['NewTerms'] = parse_response['new_terms']
                request.session['NewUsers'] = parse_response['new_users']
                request.session['NewImages'] = parse_response['new_images']
                request.session['NewFiles'] = parse_response['new_files']

                return redirect('uw_file_io.views.add_terms')
        elif request.POST['model'] == 'US':
            request.session['ImportType'] = 'User'
            try:
                request.session['NewUsers'] = parse_extract(
                    request.FILES['file_up']
                )
            except ValidationError as e:
                messages.error(
                    request,
                    str(e[0])
                )
                return redirect('uw_file_io.views.file_import')
            else:
                return redirect('uw_file_io.views.finish_import')

    message_list = _collect_messages(request)
    return render(request, 'uw_file_io/import/start.html', {
        'form': ImportForm(),
        'page_messages': message_list,
    })


@csrf_protect
def add_terms(request):
    if request.method == 'POST':
        request.session['NewTerms'] = json.loads(request.POST['termHierarchy'])

        return redirect('uw_file_io.views.add_users')

    if not request.session.get('NewTerms', None):
        return redirect('uw_file_io.views.add_users')
    return render(request, 'uw_file_io/import/new_terms.html', {
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
        return redirect('uw_file_io.views.add_images')

    if not request.session.get('NewUsers', None):
        return redirect('uw_file_io.views.add_images')

    return render(request, 'uw_file_io/import/new_users.html', {
        'new_users': request.session['NewUsers'],
        'old_users': User.objects.all(),
    })


def add_images(request):
    if request.method == 'POST':
        request.session['NewImages'] = parse_zip(
            request.FILES.get('file_up')
        )
        print request.session['NewImages']
        return redirect('uw_file_io.views.add_files')

    if not request.session.get('NewImages', None):
        return redirect('uw_file_io.views.add_files')

    return render(request, 'uw_file_io/import/file_upload.html', {
        'form': ImportForm(),
        'form_action': 'uw_file_io.views.add_images',
        'page_data': {
            'header': 'Upload Images',
            'explanation': '''It looks like one or more of the records you've
                             uploaded have associated images. Please upload a
                             *.ZIP file containing all of the image files
                             required by your records.''',
        }
    })


def add_files(request):
    if request.method == 'POST':
        request.session['NewFiles'] = parse_zip(
            request.FILES.get('file_up')
        )
        return redirect('uw_file_io.views.finish_import')

    if not request.session.get('NewFiles', None):
        return redirect('uw_file_io.views.finish_import')

    return render(request, 'uw_file_io/import/file_upload.html', {
        'form': ImportForm(),
        'form_action': 'uw_file_io.views.add_files',
        'page_data': {
            'header': 'Upload File Attachments',
            'explanation': '''It looks like one or more of the records you've
                             uploaded have associated files. Please upload a
                             *.ZIP file containing all of the files required by
                             your records.''',
        }
    })


def finish_import(request):
    item_list = request.session.get('IntermediateItems', [])
    term_list = request.session.get('NewTerms', [])
    user_list = request.session.get('NewUsers', [])
    images_list = request.session.get('NewImages', {})
    files_list = request.session.get('NewFiles', {})
    new_items = []
    transactions = []

    if isinstance(images_list, list) and len(images_list) == 0:
        images_list = {}
    elif isinstance(images_list, list):
        raise TypeError('images_list is a list instead of a dict')
    if isinstance(files_list, list) and len(files_list) == 0:
        files_list = {}
    elif isinstance(files_list, list):
        raise TypeError('files_list is a list instead of a dict')

    if request.session['ImportType'] == 'InventoryItem':
        term_to_index = process_terms_transactions(term_list, transactions)

        user_to_index = process_user_transactions(user_list, transactions)
        image_to_index = process_image_transactions(images_list, transactions)
        file_to_index = process_file_transactions(files_list, transactions)

        for item_args in item_list:
            picture_id = None
            for field in ['location_id', 'manufacturer_id', 'supplier_id']:
                if (isinstance(item_args.get(field, None), str)):
                    item_args[field] = term_to_index[item_args[field]]

            for field in ['technician_id', 'owner_id']:
                if (isinstance(item_args.get(field, None), str)):
                    item_args[field] = user_to_index[item_args[field]]

            if item_args.get('image_id', None):
                picture_id = item_args['image_id']
            item_args.pop('image_id', None)

            if item_args.get('sop_file_id', None):
                item_args['sop_file_id'] = file_to_index[
                    item_args['sop_file_id']
                ]

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
                if picture_id:
                    if isinstance(picture_id, str):
                        try:
                            picture_id = image_to_index[picture_id]
                        except KeyError:
                            print 'Image not processed {0}'.format(picture_id)
                        else:
                            image = ItemImage.objects.get(id=picture_id)
                            image.inventory_item_id = item.id
                            image.save()
                    else:
                        image = ItemImage.objects.get(id=picture_id)
                        image.inventory_item_id = item.id
                        image.save()
                if item.sop_file_id:
                    sop_file = item.sop_file
                    sop_file.inventory_item_id = item.id
                    sop_file.save()
                transactions.append(
                    'Create InventoryItem with id={0}'.format(item.id)
                )
                new_items.append(item)
    elif request.session['ImportType'] == 'User':
        for user_args in user_list:
            if isinstance(user_args, dict):
                new_user = User(**user_args)
                new_user.save()
                new_items.append(new_user)

    request.session.pop('IntermediateItems', None)
    request.session.pop('NewTerms', None)
    request.session.pop('NewUsers', None)
    request.session.pop('NewFiles', None)
    request.session.pop('NewImages', None)
    request.session.pop('ImportType', None)

    messages.success(
        request,
        'Import successful. {0} records created'.format(len(new_items))
    )

    message_list = _collect_messages(request)
    return render(request, 'uw_file_io/import/done.html', {
        'item_list': new_items,
        'page_messages': message_list,
    })


@csrf_protect
def choose_filetype(request):
    if request.method == 'POST':
        saved_models = ''

        if 'export_inventory_item' in request.POST:
            saved_models += '{0},'.format(
                request.POST['export_inventory_item']
            )
        if 'export_item_image' in request.POST:
            saved_models += '{0},'.format(
                request.POST['export_item_image']
            )
        if 'export_item_file' in request.POST:
            saved_models += '{0},'.format(
                request.POST['export_item_file']
            )
        request.session['filetype'] = request.POST.get('filetype', 'csv')
        request.session['export_models'] = saved_models
        return redirect('uw_file_io.views.finish_export')
    return render(request, 'uw_file_io/export/choose_type.html', {})


def __unicode_encode_if_string(val):
    if isinstance(val, str) or isinstance(val, unicode):
        return unicode(val).encode('utf-8')
    else:
        return val

MODEL_LOOKUP = {
    'inventory_item': InventoryItem,
    'item_file': ItemFile,
    'item_image': ItemImage,
}


def finish_export(request):
    export_models = request.session['export_models'].split(',')[:-1]

    with zipfile.ZipFile('extract.zip', 'w') as archive:
        for model in export_models:
            data_set = MODEL_LOOKUP[model].objects.all()
            filename = '{0}temp/{1}.csv'.format(settings.MEDIA_URL, model)
            with open(filename, 'w+b') as f:
                writer = csv.writer(f)

                headers = MODEL_LOOKUP[model]._meta.get_all_field_names()
                writer.writerow(headers)

                for item in data_set:
                    row = []
                    for field in headers:
                        cell = getattr(item, field, '')

                        if cell:
                            if callable(cell):
                                cell = cell()
                            if unicode(cell):
                                cell = unicode(cell).encode('utf-8')
                        row.append(cell)

                    writer.writerow(row)
                    if model in ['item_file', 'item_image']:
                        archive.write(
                            item.file_field.file.name,
                            '{0}s/{1}'.format(
                                model[5:],
                                os.path.basename(item.file_field.file.name)
                            )
                        )
            archive.write(filename, os.path.basename(filename))
