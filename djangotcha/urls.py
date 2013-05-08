from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

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
    url(r'^signin/$', 'djangotcha.views.signin', name='signin'),
    url(r'^authorized/$', 'djangotcha.views.authorized', name='authorized'),
)

urlpatterns += patterns('',
    url(r'^404/', 'citylife_website.views.error404', name='error404'),
    url(r'^500/', 'citylife_website.views.error500', name='error500'),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
)

urlpatterns += staticfiles_urlpatterns()
