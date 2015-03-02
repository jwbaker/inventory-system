import os

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

import pyexcel
import pyexcel.ext.xlsx

from uw_file_io.forms import ImportForm
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


def __get_autocomplete_term_or_insert(name, kind):
    try:
        var = AutocompleteData.objects.get(
            name__iexact=name,
            kind=kind
        )
    except AutocompleteData.DoesNotExist:
        var = AutocompleteData(name=name, kind=kind)
        var.save()
    return var


@csrf_protect
def file_import(request):
    if request.method == 'POST':
        extension = request.FILES['file_up'].name.split('.')[1]
        try:
            sheet = pyexcel.load_from_memory(
                extension,
                request.FILES['file_up'].read(),
                name_columns_by_row=0
            )
        except NotImplementedError:
            messages.error(
                request,
                '''Invalid file type {0}. Please upload one of: xls, xlsx, csv.
                '''.format(extension)
            )
        else:
            data = sheet.to_records()
            for row in data:
                if row['ID']:
                    error = False
                    # If saving goes south, we're going to want to back out of
                    # any datatabse changes, so keep track of them
                    inserted_rows = []
                    kwargs = {}

                    location = __get_autocomplete_term_or_insert(
                        row['Location'],
                        'location'
                    )
                    kwargs['location_id'] = location.id
                    inserted_rows.append(location)

                    manufacturer = __get_autocomplete_term_or_insert(
                        row['Manufacturer'],
                        'manufacturer'
                    )
                    kwargs['manufacturer_id'] = manufacturer.id
                    inserted_rows.append(manufacturer)

                    # Now for the flat fields
                    for (col, val) in row.iteritems():
                        if col in [
                            'Attachements',
                            'ID',
                            'Location',
                            'Manufacturer',
                            'Technician',
                            'Owner',
                            'SOP',
                            'Picture',
                            'Lifting_Device_Inspected_By',
                        ]:
                            continue
                        elif col in [
                            'CSA_Required',
                            'Factory_CSA',
                            'CSA_Special',
                            'Modified_Since_CSA',
                        ]:
                            kwargs[col.lower()] = (
                                True if val == 'yes' else False
                            )
                        elif col == 'Apparatus':
                            kwargs['name'] = val or None
                        elif col == 'Model':
                            kwargs['model_number'] = val or None

                    item = InventoryItem(**kwargs)
                    try:
                        item.save()
                    except IntegrityError:
                        # Back out of all changes so far
                        map(lambda x: x.delete(), inserted_rows)
                        messages.error(
                            request,
                            '''Failed to insert row {0}. Please look at your file
                            and try again.'''.format(row['ID'])
                        )
                        error = True
                        break  # Kill the loop
                    else:
                        inserted_rows.append(item)
                if not error:
                    messages.success(request, 'Import successful')
                    return HttpResponseRedirect('/list')

    message_list = _collect_messages(request)
    return render(request, 'uw_file_io/import.html', {
        'form': ImportForm(),
        'page_messages': message_list,
    })
