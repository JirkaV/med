# Django settings for med project.

import os

try:
    from local_settings import DEBUG
except ImportError:
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jirka Vejrazka', 'Jirka.Vejrazka@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'med.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Prague'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

MEDIA_ROOT = os.path.split(__file__)[0] + '/media/'
MEDIA_URL = '/media/'

STATIC_URL = '/static/med/'
STATIC_ROOT = os.path.split(__file__)[0] + '/static/'
STATICFILES_DIRS = (
    os.path.split(__file__)[0] + '/static-files/',

)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)


#ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 's%mp1e)ut7pa26n3pdu6yr7utgl%p+n@cc(6$4*l3ve2+4f=zt'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'med.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',  # for admin
    'django.core.context_processors.debug',  # {{ if debug }}
    'django.core.context_processors.media',  # for {{ MEDIA_URL }} in templates
    'django.core.context_processors.static',  # for {{ STATIC_URL }} in templates
    'django.contrib.messages.context_processors.messages',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dajaxice',
    'dajax',
    'dna',
    'glukokortikoidy',
    'cmv',
)

DAJAXICE_MEDIA_PREFIX = 'dajaxice'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
#     'root': {
#         'level': 'WARNING',
#         'handlers': ['sentry'],
#     },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'generic': {
            'format': '%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'class': 'logging.Formatter',
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'error_file': {
            'class': 'logging.FileHandler',
            'formatter': 'generic',
            'filename': '/var/log/gunicorn.error.log',
        },
        'access_file': {
            'class': 'logging.FileHandler',
            'formatter': 'generic',
            'filename': '/var/log/gunicorn.access.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'error_file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'gunicorn.error': {
            'level': 'INFO',
            'handlers': ['error_file'],
            'propagate': True,
        },
        'gunicorn.access': {
            'level': 'INFO',
            'handlers': ['access_file'],
            'propagate': False,
        },
    },
}

# I really don't want to rewrite stuff now, keep the old serializer
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# import local settings such as FORCE_SCRIPT_NAME
try:
    from local_settings import *
except ImportError:
    pass
