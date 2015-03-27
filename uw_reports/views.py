import json

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from uw_reports.forms import ReportForm
from uw_reports.models import Report
from uw_reports.parse import infix_to_postfix
from uw_inventory.forms import ItemForm
from uw_inventory.models import InventoryItem


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


@csrf_protect
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report_data = json.loads(form.cleaned_data['report_data'])
            report = form.save(commit=False)
            report_data['query'] = infix_to_postfix(
                report_data['query']
            )
            report.report_data = report_data
            report.save()

            return redirect('uw_reports.views.create_report')
        else:
            raise ValidationError(form.errors)
    message_list = _collect_messages(request)
    form = ReportForm()
    return render(request, 'uw_reports/reports_add.html', {
        'page_messages': message_list,
        'form': form,
        'form_id': 'report-form',
        'can_edit': True,
        'can_add': True,
        'field_list': ItemForm.FIELD_LIST,
        'choice_fields': {
            'status': [{k: v} for (k, v) in InventoryItem.STATUS_CHOICES]
        }
    })
