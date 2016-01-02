# coding=utf-8

from django.conf.urls import url
from .views import get_listaziende
__author__ = 'Sig'


urlpatterns = [
    url(r'^api/get_listaziende$', get_listaziende, name='get_listaziende'),
]
