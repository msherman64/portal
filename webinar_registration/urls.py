from __future__ import absolute_import
from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'webinar_registration.views',
    url(r'^$', 'index', name='index'),
    url(r'^webinar/(?P<id>\d+)/$', 'webinar', name='webinar'),
    url(r'^webinar/(?P<id>\d+)/register/$', 'register', name='register'),
    url(r'^webinar/(?P<id>\d+)/unregister/$', 'unregister', name='unregister'),
)
