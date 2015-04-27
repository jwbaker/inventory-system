from django.conf.urls import patterns, url

from uw_reports import views

urlpatterns = patterns(
    '',
    url(r'^$', views.reports_list),
    url(r'^add$', views.create_report),
    url(r'^run$', views.run_report),
    url(r'delete$', views.delete_report),
    url(r'^(?P<report_id>\d+)$', views.view_report),
    url(r'^(?P<report_id>\d+)/edit$', views.create_report),
)
