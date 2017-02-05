"""
Django settings for InvoiceGen project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Application definition
SECRET_KEY = 'X&WF+>=ml9-7sfJ_*+!H]`BvZfkI<>:X.Rsh+v87vZ|YUGl/_e'
ALLOWED_HOSTS = ['*']
DEBUG = True
COMMUNICATION_KEY = '28359ruioterhfweuith34tlkjre'
ROOT_HOSTCONF = 'InvoiceGen.hosts'
DEFAULT_HOST = 'www'
SHARED_APPS = (
    'tenant_schemas',  # mandatory, should always be before any django app
    'Tenants', # you must list the app where your tenant model resides in
    'django.contrib.contenttypes',
    # everything below here is optional
    'channels',
    'Blog',
    'PaymentProcessor',
)

TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'django.contrib.humanize',
    # your tenant-specific apps
    'Orders',
    'Agreements',
    'Invoices',
    'Companies',
    'Settings',
    'Todo',
    'HourRegistration',
    'Statistics',
    'Mail',
)

INSTALLED_APPS = (
    'tenant_schemas',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'Orders',
    'Agreements',
    'Invoices',
    'Companies',
    'Settings',
    'django_bootstrap_breadcrumbs',
    'Todo',
    'HourRegistration',
    'Statistics',
    'Mail',
    'django_tables2',
    'django.contrib.humanize',
    'channels',
    'Tenants',
    'Blog',
    'PaymentProcessor',
    'django_hosts'
)
TENANT_MODEL = "Tenants.Client"

# In settings.py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",  # use redis backend
        "CONFIG": {
           "hosts": [os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')],  # set redis address
         },
        "ROUTING": "InvoiceGen.routing.channel_routing",
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending e-mail.
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'no-reply@invoicegen.nl'

MIDDLEWARE_CLASSES = (
    'django_hosts.middleware.HostsRequestMiddleware',
    'tenant_schemas.middleware.TenantMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
    #'Orders.middleware.OrderMiddleware',
)

ROOT_URLCONF = 'InvoiceGen.urls'

WSGI_APPLICATION = 'InvoiceGen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': 'invoicegen',
    }
}

DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

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
MEDIA_ROOT = BASE_DIR + '/static/files/'
MEDIA_URL = '/files/'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
