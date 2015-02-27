import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

import pyexcel
import pyexcel.ext.xlsx

from uw_file_io.forms import ImportForm
from uw_inventory.models import (
    InventoryItem,
    ItemFile
)


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
        extension = request.FILES['file_up'].name.split('.')[1]
        sheet = pyexcel.load_from_memory(
            extension,
            request.FILES['file_up'].read(),
            name_columns_by_row=0
        )
        data = sheet.to_records()
        for row in data:
            kwargs = {}

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
                    kwargs[col.lower()] = True if val == 'yes' else False
                elif col == 'Apparatus':
                    kwargs['name'] = val

            item = InventoryItem(**kwargs)
            item.save()
        return HttpResponseRedirect('/list')

    return render(request, 'uw_file_io/import.html', {
        'form': ImportForm(),
    })
