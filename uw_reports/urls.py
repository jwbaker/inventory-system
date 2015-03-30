from django.conf.urls import patterns, url

from uw_reports import views

urlpatterns = patterns(
    '',
    url(r'^$', views.reports_list),
    url(r'^add$', views.create_report),
    url(r'^run$', views.run_report),
)
