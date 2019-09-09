from __future__ import absolute_import
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'tas.views',
    url(r'^forgot-username/$', 'recover_username', name='recover_username'),
    url(r'^register/$', 'register', name='register'),
    url(r'^password-reset/$', 'password_reset', name='password_reset'),
    url(r'^email-confirmation/$', 'email_confirmation', name='email_confirmation'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^profile/edit/$', 'profile_edit', name='profile_edit'),
    url(r'^departments\.json$', 'get_departments_json'),
)
