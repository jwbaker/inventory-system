from django.conf.urls import patterns, url

from uw_inventory import views

urlpatterns = patterns(
    '',
    url(r'^$', views.inventory_list),
    url(r'^add$', views.inventory_add),
    url(r'^autocomplete/add/$', views.autocomplete_new),
    url(r'^autocomplete/(?P<source>.*)$', views.autocomplete_list),
    url(r'^note/add$', views.note_new),
    url(r'^(?P<item_id>\d+)$', views.inventory_detail),
    url(r'^(?P<item_id>\d+)/duplicate$', views.inventory_copy),
    url(r'^(?P<item_id>\d+)/delete$', views.inventory_delete),
    url(r'^(?P<item_id>\d+)/restore$', views.inventory_undelete),
)
