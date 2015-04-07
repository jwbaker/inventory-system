from django.conf.urls import patterns, url

from uw_file_io import views

urlpatterns = patterns(
    '',
    url(r'^download/(?P<file_id>\d+)/$', views.file_download),
    url(r'^(?P<file_name>media/files/.+)/$', views.file_view),
    url(r'^import/$', views.file_import),
    url(r'^import/add-terms/$', views.add_terms),
    url(r'^import/add-users/$', views.add_users),
    url(r'^import/add-images/$', views.add_images),
    url(r'^import/add-files/$', views.add_files),
    url(r'^import/done/$', views.finish_import),
    url(r'^export/choose-type/$', views.choose_filetype),
    url(r'^export/done/$', views.finish_export),
)
