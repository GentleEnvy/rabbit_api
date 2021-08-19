import json
from pathlib import Path
import os

import django_heroku

from api.logs.configs import LogConfig
from api.logs.configs.handlers import *

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False if (_debug := os.getenv('DJANGO_DEBUG')) is None else bool(int(_debug))

INTERNAL_IPS = [
    '127.0.0.1'
]

# noinspection SpellCheckingInspection
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'model_utils',
    'simple_history',
    'debug_toolbar',
    
    'api.apps.ApiConfig'
]

# noinspection SpellCheckingInspection
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api.paginations.base.BasePagination',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ]
}

CORS_ALLOW_ALL_ORIGINS = True

# noinspection SpellCheckingInspection
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    
    'api.middlewares.RequestLogMiddleware',
    'api.middlewares.NotEmptyResponseMiddleware'
]

ROOT_URLCONF = 'rabbit_api.urls'

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
            ]
        }
    }
]

WSGI_APPLICATION = 'rabbit_api.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator'
    }, {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    }, {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    }, {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    }
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

FIXTURE_DIRS = ['api/tests/fixtures/']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMINS = [('envy', 'envy15@mail.ru'), ('envy', 'komarov.sergei163@gmail.com')]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

###
# Custom

TEST = False if (_test := os.getenv('DJANGO_TEST')) is None else bool(int(_test))
YANDEX_DISK_TOKEN = os.getenv('YANDEX_DISK_TOKEN')

# Custom
###

if DEBUG:  # dev
    LOGGING = LogConfig(
        {
            'api': {'handlers': [api_file, api_console]},
            'gunicorn.access': {'handlers': [web_file]}
        }
    ).to_dict()
elif TEST:  # test
    LOGGING = LogConfig(
        {
            'api': {'handlers': [api_console]},
            'django.server': {'handlers': [web_console]}
        }
    ).to_dict()
else:  # prod
    LOGGING = LogConfig(
        {
            'api': {'handlers': [api_file, api_console, email_admins]},
            'gunicorn.access': {'handlers': [web_file]}
        }
    ).to_dict()

###
# Heroku

SECRET_KEY = '''<django_heroku>'''
ALLOWED_HOSTS = '''<django_heroku>'''
DATABASES = {'default': ''''<django_heroku>'''}

django_heroku.settings(locals(), test_runner=False, logging=False)

# Heroku
###
