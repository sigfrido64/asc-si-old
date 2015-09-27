# coding=utf-8

from django.conf.urls import patterns, url
from .views import index, get_corsi, add_edit


urlpatterns = patterns('',
                       url(r'^$', index, name='index'),
                       url(r'^add/$', add_edit, name='add'),
                       url(r'^edit/(?P<pk>\w+)$', add_edit, name='edit'),
                       url(r'^api/get_corsi$', get_corsi, name='get_corsi'),
                       )
