from django.conf.urls import patterns, url

from uw_file_io import views

urlpatterns = patterns(
    '',
    url(r'^download/(?P<file_id>\d+)/$', views.file_download),
    url(r'^(?P<file_name>files/.+)/$', views.file_view),
    url(r'^import/$', views.file_import),
    url(r'^import/add-terms/$', views.add_terms),
    url(r'^import/add-users/$', views.add_users),
    url(r'^import/done/$', views.finish_import),
)
