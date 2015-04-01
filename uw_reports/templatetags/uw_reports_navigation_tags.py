from django import template
from django.db.models import Q

from uw_reports.models import Report

register = template.Library()


@register.inclusion_tag('uw_reports/context_menu.html')
def reports_context_menu(user):
    if user.has_perm('uw_reports.view_all_reports'):
        reports = Report.objects.all().order_by(
            '-view_count', '-creation_date'
        )[:5]
    else:
        reports = Report.objects.filter(
            Q(creator=user) |
            Q(creator__isnull=True)
        ).order_by('-view_count', '-creation_date')[:5]

    return {
        'user': user,
        'reports': reports,
        'can_add': user.has_perm('uw_reports.add_report')
    }
