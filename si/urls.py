# coding=utf-8
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from .views import about, index, user_login, user_logout
from django.contrib.auth import views as auth_views


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'si.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^', include('docusign.urls')),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^si/$', index, name="index"),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^about/$', about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^si/iniziative/', include('iniziative.urls', namespace="iniziative", app_name="iniziative")),
    url(r'^si/fs/', include('sifilesmanager.urls', namespace="fs", app_name="fs")),
    url(r'^si/corsi/', include('corsi.urls', namespace="corsi", app_name="corsi")),
    url(r'^si/segnalazioni/', include('segnalazioni.urls', namespace="segnalazioni", app_name="segnalazioni")),
    url(r'^si/op/', include('op.urls', namespace="op", app_name="op")),
    url(r'^si/aziende/', include('aziende.urls', namespace="aziende", app_name="aziende")),
    ) + static(settings.SIFILEDATA_URL, document_root=settings.SIFILEDATA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
