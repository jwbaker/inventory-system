from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'uw_inventory_system.views.home',
                       #     name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', lambda r: HttpResponseRedirect('list/')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^list/', include('uw_inventory.urls')),
                       )
