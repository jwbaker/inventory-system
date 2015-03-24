from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render

from uw_reports.models import Report


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


def reports_list(request):
    message_list = _collect_messages(request)
    if request.user.has_perm('uw_reports.view_all_reports'):
        reports_list = Report.objects.all()
    else:
        reports_list = Report.objects.filter(
            Q(report_owner__exact=request.user.username) |
            Q(report_owner__exact=None)
        )
    return render(request, 'uw_reports/reports_list.html', {
        'reports_list': reports_list,
        'page_messages': message_list,
    })
