# coding=utf-8
__author__ = 'Sig'
from django.conf.urls import patterns, url
from corsi import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),)
