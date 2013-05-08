from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from utilities.language import set_language


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = i18n_patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'djangotcha.views.home', name='home'),
    url(r'^login/$', 'djangotcha.views.login', name='login'),
    url(r'^complete/github/$', 'djangotcha.views.authorized', name='authorized'),
    url(r'^profile/$', 'djangotcha.views.profile', name='profile'),

    # Social auth
    url(r'', include('social_auth.urls')),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^404/', 'djangotcha.views.error404', name='error404'),
    url(r'^500/', 'djangotcha.views.error500', name='error500'),
)

urlpatterns += staticfiles_urlpatterns()
