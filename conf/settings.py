"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import pathlib
import datetime
from envparse import env

env.read_envfile()

# Base path
BASE_PATH = pathlib.Path(__file__).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

SECRET_KEY = env('SECRET_KEY', cast=str, default='f)x_76pg46@omifv%=f0evs(4fiqkbr_k1p%nld2qtey8dyoc(')

DEBUG = env('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]

THIRD_PARTY_APPS = [
    'raven.contrib.django.raven_compat',
    'debug_toolbar',
]

LOCAL_APPS = [
    'apps.logger',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SITE_ID = 1

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB_NAME', default=''),
        'USER': env('POSTGRES_DB_USER', default=''),
        'PASSWORD': env('POSTGRES_DB_PASSWORD', default=''),
        'HOST': env('POSTGRES_DB_HOST', default=''),
        'PORT': env('POSTGRES_DB_PORT', default=''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_PATH / 'static')

# Media files (Images, Video, pdf, etc)
MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_PATH / 'media')

# Data upload
DATA_UPLOAD_MAX_NUMBER_FIELDS = 25000
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440 * 4

### Application logging
import raven
LOG_LEVEL = env('LOG_LEVEL', cast=str, default='INFO').upper()
RAVEN_DSN = env.str('RAVEN_DSN', default='')
RAVEN_CONFIG = {
    'dsn': RAVEN_DSN,
    'release': raven.fetch_git_sha(BASE_PATH),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'syslog': {
            'format': '%(levelname)s <PID %(process)d> '
                      '%(name)s.%(funcName)s(): %(message)s'
        },
        'verbose': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(levelname) -10s %(asctime)s '
                      '%(processName) -35s %(name) -35s '
                      '%(funcName) -30s %(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console', 'sentry'],
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'apps.logger': {
            'level': LOG_LEVEL,
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    },
}


# Debugtoolbar
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

CONFIG_DEFAULTS = {
    # Toolbar options
    'RESULTS_CACHE_SIZE': 3,
    'SHOW_COLLAPSED': True,
    'SQL_WARNING_THRESHOLD': 500,
}
