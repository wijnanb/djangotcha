# Django settings for citylife_website project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# path_to
import os
ROOT = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
path_to = lambda *x: os.path.join(ROOT, *x)

# Debugging: disable cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

ADMINS = ( )
MANAGERS = ADMINS


MAIL_PRESS = "press@citylifeapp.com"

TIME_ZONE = 'Europe/Brussels'

LANGUAGE_CODE = 'en-us'
SOURCE_LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en', 'EN'),
    ('fr', 'FR'),
    ('nl', 'NL'),
)

LOCALE_PATHS = [ os.path.join(ROOT, 'locale') ]

LOCALEURL_USE_ACCEPT_LANGUAGE = True
SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ( )

# SESSION_FILE_PATH = 'path_to_store_sessions_file'
SESSION_ENGINE = 'django.contrib.sessions.backends.file'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangotcha',
        'USER': 'root',
        'PASSWORD': ''
    }
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'Hq(Z7uQ{X3_F+r0xg21i4b?5-8>DBp(+57$<y/TB2o=3T_r{mW3.r6A0q0fob'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'djangotcha.urls'

TEMPLATE_DIRS = (
    'templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_template_tags',
    'django.contrib.admin',
    'social_auth',
    'djangotcha',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.github.GithubBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/profile/'
LOGIN_ERROR_URL    = '/login-error/'

# Develop app: https://github.com/settings/applications/44683
GITHUB_APP_ID              = '157475f917973a32b319'
GITHUB_API_SECRET          = '3c49aabd451267a8a9a53791b6df6ebd56703343'
GITHUB_REQUEST_TOKEN_URL   = 'https://github.com/login/oauth/access_token'

SECRET_WORDS = [
    'word1', 'word2', 'word3', 'word4', 'word5'
]

# The absolute location of this website
SERVER_LOCATION = 'http://localhost:8000/'

execfile(path_to('djangotcha', 'settings_local.py'))
