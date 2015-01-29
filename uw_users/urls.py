from django.conf.urls import patterns, url

from uw_users import views

urlpatterns = patterns(
    '',
    url(r'^$', views.user_list),
    url(r'^login/$', 'django_cas.views.login'),
    url(r'^logout/$', 'django_cas.views.logout'),
    url(r'^(?P<username>\w*)$', views.user_detail),
)
