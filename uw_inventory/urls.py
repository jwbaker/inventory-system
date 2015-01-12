from django.conf.urls import patterns, url

from uw_inventory import views

urlpatterns = patterns(
    '',
    url(r'^$', views.inventory_list),
    url(r'^(?P<item_id>\d+)$', views.inventory_detail),
)
