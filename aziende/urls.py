# coding=utf-8
__author__ = 'Sig'
from django.conf.urls import patterns, url
from .views import get_listaziende


urlpatterns = patterns('',
                       url(r'^api/get_listaziende$', get_listaziende, name='get_listaziende'),
                       )
