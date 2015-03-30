from django import template
from django.db.models import Q

from uw_reports.models import Report

register = template.Library()


@register.inclusion_tag('uw_reports/context_menu.html')
def reports_context_menu(user):
    reports = Report.objects.filter(
        Q(creator=user) |
        Q(creator__isnull=True)
    ).order_by('-view_count', '-creation_date')[:5]

    return {
        'user': user,
        'reports': reports
    }
