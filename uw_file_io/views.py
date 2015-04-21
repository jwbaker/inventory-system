import csv
import json
import os
import zipfile

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from django_cas.decorators import permission_required

from uw_file_io.forms import ImportForm
from uw_file_io.parse import (
    process_extract,
    process_terms_transactions,
    process_user_transactions,
    import_data,
)
from uw_inventory.models import (
    AutocompleteData,
    InventoryItem,
    ItemFile,
    ItemImage
)
from uw_reports.models import Report
from uw_reports.parse import postfix_to_query_filter


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
    request.session.pop('extract_data', None)
    request.session.pop('new-terms', None)
    request.session.pop('new-users', None)

    if request.method == 'POST':
        extract_data = process_extract(
            request.FILES.get('file_up', None)
        )
        request.session['extract_data'] = extract_data
        return redirect('uw_file_io.views.add_terms')
    message_list = _collect_messages(request)
    return render(request, 'uw_file_io/import/start.html', {
        'form': ImportForm(),
        'page_messages': message_list,
    })


@csrf_protect
def add_terms(request):
    if request.method == 'POST':
        request.session['new-terms'] = json.loads(request.POST['termHierarchy'])

        return redirect('uw_file_io.views.add_users')

    extract_data = request.session['extract_data']
    terms_data = {k: v for k, v in extract_data['new_terms'].items() if
                  k in ['location', 'manufacturer', 'supplier'] and len(v) > 0}
    if not terms_data:
        return redirect('uw_file_io.views.add_users')

    old_terms = {}

    for k in terms_data.keys():
        old_terms[k] = AutocompleteData.objects.filter(kind=k)
    return render(request, 'uw_file_io/import/new_terms.html', {
        'new_terms': terms_data,
        'old_terms': old_terms,
    })


@csrf_protect
def add_users(request):
    if request.method == 'POST':
        request.session['new-users'] = json.loads(request.POST['userHierarchy'])

        return redirect('uw_file_io.views.finish_import')

    extract_data = request.session['extract_data']
    terms_data = reduce(
        lambda x, y: x.append(y),
        [v for k, v in extract_data['new_terms'].items() if
         k in ['owner', 'technician']],
        []
    )
    if not terms_data:
        return redirect('uw_file_io.views.finish_import')

    old_users = User.objects.all()

    return render(request, 'uw_file_io/import/new_users.html', {
        'new_users': terms_data,
        'old_users': old_users,
    })


def finish_import(request):
    extract_data = request.session.pop('extract_data', None)
    new_terms = request.session.pop('new-terms', [])
    new_users = request.session.pop('new-users', [])

    term_to_index = process_terms_transactions(new_terms)
    user_to_index = process_user_transactions(new_users)

    new_items = import_data(
        extract_data['model_data'],
        term_to_index,
        user_to_index
    )

    message_list = _collect_messages(request)
    return render(request, 'uw_file_io/import/done.html', {
        'item_list': new_items,
        'page_messages': message_list,
    })


@csrf_protect
def export_options(request, report_id=''):
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
        request.session['report_id'] = report_id
        request.session['export_models'] = saved_models
        return redirect('uw_file_io.views.finish_export')
    if report_id:
        form_action = reverse(
            'uw_file_io.views.export_options', args=[report_id]
        )
    else:
        form_action = reverse('uw_file_io.views.export_options')
    return render(request, 'uw_file_io/export/choose_type.html', {
        'form_action': form_action
    })


MODEL_LOOKUP = {
    'inventory_item': InventoryItem,
    'item_file': ItemFile,
    'item_image': ItemImage,
}


def __export_model(Model, report_id):
    data_set = __package_export_dataset(Model, report_id)
    headers = Model._meta.get_all_field_names()
    filename = 'media/temp/{0}.csv'.format(Model.__name__.lower())
    file_list = []

    with open(filename, 'w+b') as extract:
        writer = csv.writer(extract)
        writer.writerow(headers)

        for item in data_set:
            row = []
            for field in headers:
                cell = getattr(item, field, '')

                if callable(cell):
                    cell = cell()
                if unicode(cell):
                    cell = unicode(cell).encode('utf-8')

                if field == 'file_field':
                    file_list.append(cell)
                    cell = cell
                row.append(cell)
            writer.writerow(row)
    print file_list
    zipfile_name = 'media/temp/{0}.zip'.format(Model.__name__.lower())

    with zipfile.ZipFile(zipfile_name, 'w') as archive:
        archive.write(filename, os.path.basename(filename))

        for f in file_list:
            archive.write(f, f)

    return zipfile_name


def __package_export_dataset(Model, report_id):
    if report_id:
        report = Report.objects.get(id=report_id)
        items = InventoryItem.objects.filter(
            postfix_to_query_filter(json.loads(report.report_data)['query'])
        )

        if Model is InventoryItem:
            return items
        else:
            return Model.objects.filter(
                inventory_item_id__in=[i.id for i in items]
            )
    else:
        return Model.objects.all()


@csrf_protect
def finish_export(request):
    if request.method == 'POST':
        archive_name = request.session.pop('export_filename')

        with open(archive_name, 'r') as archive:
            response = HttpResponse(archive)
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
                os.path.basename(archive_name)
            )

            return response

    export_models = request.session.pop('export_models').split(',')[:-1]
    report_id = request.session.pop('report_id')

    model_zipfiles = [__export_model(MODEL_LOOKUP[model], report_id) for
                      model in export_models]

    archive_name = 'media/temp/extract.zip'

    with zipfile.ZipFile(archive_name, 'w') as archive:
        for zf_name in model_zipfiles:
            with zipfile.ZipFile(zf_name, 'r') as model_archive:
                for name in model_archive.namelist():
                    temp = model_archive.open(name)
                    archive.writestr(name, temp.read())
            os.remove(zf_name)

    request.session['export_filename'] = archive_name

    return render(request, 'uw_file_io/export/done.html', {})
