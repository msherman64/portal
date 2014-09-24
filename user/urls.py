
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_change, password_change_done

import user.views
from user.forms import ChameleonPasswordChangeForm

urlpatterns = patterns('',
    url(r'^login/$', login, {"template_name": "user/login.html"}),
    url(r'^logout/$', logout, {"next_page" : "/"}),
    #url(r'^logout/$', logout, {"next_page" : "user/logged_out.html"}),
    #url(r'^logged_out.html$', user.views.logged_out),

    url(r'^password_change/$', password_change,
        {"template_name": "user/password_change_form.html",
         "password_change_form": ChameleonPasswordChangeForm,
         "post_change_redirect": "/user/password_change_done"}),

    url(r'^password_change_done$', password_change_done, 
        {"template_name": "user/password_change_done.html"}),

    url(r'^password_reset/', include('password_reset.urls')),

    url(r'^request/$', user.views.request_account),
    url(r'^review/$', user.views.account_requests),
    url(r'^review/approved/$', user.views.approve_request),
    url(r'^review/denied/$', user.views.deny_request),
    url(r'^review/user/(?P<username>\S+)/$', user.views.approve_account, name="profile"),

    #url(r'^profile/$', user.views.profile),
    #url(r'^profile/(?P<pk>\S+)/$', user.views.UserView.as_view(), name='user'),

)


# password reset starts at user/password_reset/recover/
