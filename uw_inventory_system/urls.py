from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect

from uw_inventory_system import views

urlpatterns = patterns(
    '',
    url(r'^$', lambda r: HttpResponseRedirect('list/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^list/', include('uw_inventory.urls')),
    # url(r'^accounts/login/$', 'django_cas.views.login'),
    # url(r'^accounts/logout/$', 'django_cas.views.logout'),
    url(r'^accounts/', include('uw_users.urls')),
    # TODO: remove this URL for production
    url(r'^forbidden/$', views.permission_denied),
    url(r'^download/(?P<file_id>\d+)/$', views.file_download),
    url(r'^(?P<file_name>files/.+)/$', views.file_view),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
