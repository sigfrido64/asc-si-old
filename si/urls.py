# coding=utf-8
from django.conf import settings

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

from .views import about, index, user_login, user_logout

from sifilesmanager.views import fileupload

# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'si.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^', include('docusign.urls')),

    url(r'^si/$', index, name="index"),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^about/$', about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^corsi/', include('corsi.urls', namespace="corsi", app_name="corsi")),
    url(r'^si/iniziative/', include('iniziative.urls', namespace="iniziative", app_name="iniziative")),
    url(r'^si/fs/', include('sifilesmanager.urls', namespace="fs", app_name="fs")),
    ) + static(settings.SIFILEDATA_URL, document_root=settings.SIFILEDATA_ROOT)


"""
    url(r'^$', ProfileImageIndexView.as_view(), name='home'),


    url(
        r'^uploaded/(?P<pk>\d+)/$', ProfileDetailView.as_view(),
        name='profile_image'),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""