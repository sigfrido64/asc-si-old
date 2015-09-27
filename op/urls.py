# coding=utf-8
from django.conf.urls import patterns, url
from .views import index, op_edit

urlpatterns = patterns('',
                       url(r'^$', index, name='index'),
                       url(r'^add/$', op_edit, name='add'),
                       url(r'^edit/(?P<pk>\w+)$', op_edit, name='edit'),
                       )
