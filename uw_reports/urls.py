from django.conf.urls import patterns, url

from uw_reports import views

urlpatterns = patterns(
    '',
    url(r'^$', views.reports_list)
)
