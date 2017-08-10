"""
Django settings for InvoiceGen project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

ROOT_HOSTCONF = 'InvoiceGen.hosts'

ALLOWED_HOSTS = ['*']
DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

# Host for sending e-mail.
EMAIL_HOST = 'smtp'
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = 'email@invoicegen'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'orders',
    'agreements',
    'invoices',
    'companies',
    'settings',
    'django_bootstrap_breadcrumbs',
    'hour_registration',
    'statistics',
    'mail',
    'django_tables2',
    'django.contrib.humanize',
    'channels',
    'rest_framework',
    'autoadmin'
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'InvoiceGen.urls'

WSGI_APPLICATION = 'InvoiceGen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'HOST': 'postgres',
        'USER': 'postgres',
    }
}


CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.request',
    'InvoiceGen.context_processor.website_name',
    'InvoiceGen.context_processor.color_up',
    'InvoiceGen.context_processor.color_down',
    'InvoiceGen.context_processor.attach_toast_to_response']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/templates/'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': CONTEXT_PROCESSORS,
        },
    },
]

# In settings.py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",  # use redis backend
        "CONFIG": {
           "hosts": [os.environ.get('REDIS_URL', 'redis://redis:6379')],  # set redis address
         },
        "ROUTING": "InvoiceGen.routing.channel_routing",
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
BREADCRUMBS_TEMPLATE = "breadcrumbs.html"
LANGUAGE_CODE = 'nl'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DECIMAL_SEPARATOR = ','
DEFAULT_COLOR = '#009688'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
    os.path.join(BASE_DIR, "bower_components"),
]
MEDIA_ROOT =  os.path.join(BASE_DIR, 'static/media')
MEDIA_URL = '/files/'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'invoicegen'
    }

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ]
}