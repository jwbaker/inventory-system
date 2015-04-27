import json

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_protect

from uw_reports.forms import ReportForm
from uw_reports.models import Report
from uw_reports.parse import infix_to_postfix, postfix_to_query_filter
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
            Q(owner__exact=request.user.id) |
            Q(owner__isnull=True)
        )
    return render(request, 'uw_reports/reports_list.html', {
        'reports_list': reports_list,
        'page_messages': message_list,
    })


def __create_report_test(user):
    return (
        user.has_perm('uw_reports.add_report') or
        user.has_perm('uw_reports.change_report')
    )


@csrf_protect
@user_passes_test(__create_report_test)
def create_report(request, report_id=None):
    if report_id:
        saved_report = Report.objects.get(id=report_id)
    else:
        saved_report = None

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=saved_report)
        if form.is_valid():
            report_data = json.loads(form.cleaned_data['report_data'])
            report = form.save(commit=False)
            report_data['query'] = infix_to_postfix(
                report_data['query']
            )
            report.report_data = json.dumps(report_data)
            report.creator_id = request.user.id
            report.save()
            return redirect('uw_reports.views.view_report', report_id=report.id)
        else:
            messages.error(request, 'Something went wrong')
    message_list = _collect_messages(request)
    form = ReportForm(instance=saved_report)
    return render(request, 'uw_reports/reports_add.html', {
        'page_messages': message_list,
        'form': form,
        'form_id': 'report-form',
        'form_target': reverse(
            'uw_reports.views.create_report',
            args=[report_id]
        ) if report_id else reverse('uw_reports.views.create_report'),
        'can_edit': request.user.has_perm('uw_reports.change_report'),
        'can_add': request.user.has_perm('uw_reports.add_report'),
        'field_list': ItemForm.FIELD_LIST,
        'choice_fields': {
            'status': [{k: v} for (k, v) in InventoryItem.STATUS_CHOICES]
        }
    })


@csrf_protect
def run_report(request):
    if request.is_ajax():
        postfix_query = infix_to_postfix(request.POST['query'])
        query_filter = postfix_to_query_filter(postfix_query)

        results = InventoryItem.objects.filter(query_filter)
        display_fields = request.POST.get('display_fields', '')

        return render_to_response(
            'uw_reports/report_result.html',
            {
                'results': results,
                'display_fields': display_fields.split(',')
            },
            content_type='text/html'
        )


def view_report(request, report_id):
    report = Report.objects.get(id=report_id)
    report.view_count += 1
    report.save()

    report_data_json = json.loads(report.report_data)
    query_filter = postfix_to_query_filter(report_data_json['query'])

    if query_filter:
        results = InventoryItem.objects.filter(query_filter)
    else:
        results = InventoryItem.objects.all()

    message_list = _collect_messages(request)
    return render(request, 'uw_reports/view_report.html', {
        'page_messages': message_list,
        'report': report,
        'results': results,
        'display_fields': report_data_json['display_fields'].split(',')[:-1]
    })


@csrf_protect
def delete_report(request):
    if request.is_ajax():
        report_id = request.POST.get('report_id')
        report = Report.objects.get(id=report_id)

        if (
                request.user != report.owner and
                not request.user.has_perm('uw_reports.view_all_reports')
           ):
            return HttpResponseForbidden()
        report.to_display = False
        report.save()

        return HttpResponse()
