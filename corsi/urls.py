# coding=utf-8
__author__ = 'Sig'
from django.conf.urls import patterns, url
from .views import CorsiListView


urlpatterns = patterns('',
                       url(r'^$', CorsiListView.as_view(), name='index'),)
