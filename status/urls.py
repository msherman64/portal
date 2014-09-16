
from django.conf.urls import patterns, url

from status import views

urlpatterns = patterns('',
    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\S+)/$', views.DetailView.as_view(), name='detail'),
)
