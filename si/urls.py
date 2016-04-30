# coding=utf-8
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from .views import index
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Examples:
    # url(r'^$', 'si.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^', include('docusign.urls')),
    url(r'^si/$', index, name="index"),
    url(r'^si/login/$', auth_views.login, name='login'),
    url(r'^si/logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^si/passchange/$', auth_views.password_change, {'post_change_redirect': '/si/'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^si/iniziative/', include('iniziative.urls', namespace="iniziative", app_name="iniziative")),
    url(r'^si/fs/', include('sifilesmanager.urls', namespace="fs", app_name="fs")),
    url(r'^si/corsi/', include('corsi.urls', namespace="corsi", app_name="corsi")),
    url(r'^si/segnalazioni/', include('segnalazioni.urls', namespace="segnalazioni", app_name="segnalazioni")),
    url(r'^si/op/', include('op.urls', namespace="op", app_name="op")),
    url(r'^si/aziende/', include('aziende.urls', namespace="aziende", app_name="aziende"))
] + static(settings.SIFILEDATA_URL, document_root=settings.SIFILEDATA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
