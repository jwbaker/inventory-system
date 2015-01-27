from django.http import HttpResponseForbidden

from uw_inventory_system.views import permission_denied


class Forbidden403(object):
    def process_response(self, request, response):
        if isinstance(response, HttpResponseForbidden):
            return permission_denied(request)
        else:
            return response
