import os
import django
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth import views as auth_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

# Serve the static content of the admin
# http://stackoverflow.com/questions/6984672/django-admin-site-not-formatted
admin_media_path = os.path.join(django.__path__[0], 'contrib', 'admin', 'static', 'admin')

urlpatterns = patterns('',
    url(r'^$', 'djangotcha.views.home', name='home'),
    url(r'^login/$', 'djangotcha.views.login', name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^complete/github/$', 'djangotcha.views.authorized', name='authorized'),

    url(r'^kill/(?P<user_id>\d+)$', 'djangotcha.views.kill', name='kill'),
    url(r'^rules/$', 'djangotcha.views.rules', name='rules'),
    url(r'^closed/$', 'djangotcha.views.closed', name='closed'),

    # Social auth
    url(r'', include('social_auth.urls')),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': admin_media_path,
        }),
)

urlpatterns += patterns('',
    url(r'^404/', 'djangotcha.views.error404', name='error404'),
    url(r'^500/', 'djangotcha.views.error500', name='error500'),
)

urlpatterns += staticfiles_urlpatterns()


