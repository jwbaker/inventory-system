from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect

from uw_inventory_system import views
from uw_inventory.api import InventoryItemResource

inventory_item_resource = InventoryItemResource()

urlpatterns = patterns(
    '',
    url(r'^$', lambda r: HttpResponseRedirect('list/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^list/', include('uw_inventory.urls')),
    url(r'^accounts/', include('uw_users.urls')),
    # TODO: remove this URL for production
    url(r'^forbidden/$', views.permission_denied),
    url(r'^files/', include('uw_file_io.urls')),
    url(r'^reports/', include('uw_reports.urls')),
    url(r'^api/', include(inventory_item_resource.urls)),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
