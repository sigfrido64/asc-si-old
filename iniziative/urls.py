# coding=utf-8
__author__ = 'Sig'
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from iniziative.views import IniziativaAdd, IniziativaEdit, IniziativaDelete, index, detail, sottoiniziativa_detail, \
    sottoiniziativa_add, sottoiniziativa_edit, SottoIniziativaDelete, gruppo_add, gruppo_edit, GruppoDelete, gruppo_detail


urlpatterns = patterns('',
                       url(r'^$', index, name='index'),
                       url(r'^add/$', login_required(IniziativaAdd.as_view()), name='add'),
                       url(r'^edit/(?P<pk>\d+)$', login_required(IniziativaEdit.as_view()), name='edit'),
                       url(r'^delete/(?P<pk>\d+)$', login_required(IniziativaDelete.as_view()), name='delete'),
                       url(r'^(?P<pk_iniziativa>\d+)/$', detail, name='detail'),

                       url(r'^(?P<pk_iniziativa>\d+)/subadd/$', sottoiniziativa_add, name='sub_add'),
                       url(r'^subedit/(?P<pk>\d+)$', sottoiniziativa_edit, name='sub_edit'),
                       url(r'^delete_sub/(?P<pk>\d+)$', login_required(SottoIniziativaDelete.as_view()),
                           name='sub_delete'),
                       url(r'^sub/(?P<pk_sub>\d+)/$', sottoiniziativa_detail, name='sub_detail'),

                       url(r'^(?P<pk_sub>\d+)/grpadd/$', gruppo_add, name='grp_add'),
                       url(r'^grpedit/(?P<pk>\d+)$', gruppo_edit, name='grp_edit'),
                       url(r'^delete_grp/(?P<pk>\d+)$', login_required(GruppoDelete.as_view()),
                           name='grp_delete'),
                       url(r'^grp/(?P<pk_grp>\d+)/$', gruppo_detail, name='grp_detail'),
                       )





