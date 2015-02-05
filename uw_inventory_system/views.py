import os

from django.http import HttpResponse
from django.shortcuts import render

from uw_inventory.models import ItemFile


def permission_denied(request):
    return render(request, 'errors/403.html')


def file_download(request, file_id):
    if request.method == 'GET':
        file = ItemFile.objects.get(id=file_id).file
        response = HttpResponse(file)
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            os.path.basename(file.name)
        )

        return response
