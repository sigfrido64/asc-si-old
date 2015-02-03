# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import about, index, user_login, user_logout
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
    )

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

