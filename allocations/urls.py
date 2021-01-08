from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^view/$', views.view, name='view'),
    url(r'^pending/$', views.pending, name='pending'),
    url(r'^approval/$', views.approval, name='approval'),
    url(r'^denied/$', views.denied, name='denied'),
    url(r'^user/$', views.user_select, name='user_select'),
    url(r'^user/(?P<username>.+?)/$', views.user_projects, name='user_projects'),
    url(r'^template/(?P<resource>.+?)\.html/$', views.allocations_template, name='allocations_template'),
]
