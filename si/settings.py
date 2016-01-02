# coding=utf-8
"""
Django settings for si project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/

Utente Amministrativo : admin - radice
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys


# Specifico per MongoEngine
from mongoengine import connect

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1$t)$+-ey%m0!#f!=2&pj&1^-1dfca0t4u(erl0)u54n#1-3#d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            TEMPLATE_PATH,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': True,
        },
    },
]

ALLOWED_HOSTS = []


# Application definition
# Admin password = radice
# Ho tolto 'docusign'
# Ho tolto 'localflavor' perchè sembra che non serva a nulla e crea solo problemi con Django quando parte

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'iniziative',
    'sifilesmanager',
    'corsi',
    'aziende',
    'op',
    'debug_toolbar',
    'tasker',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'si.urls'

WSGI_APPLICATION = 'si.wsgi.application'



# Connessione a MongoDB usando MongoEngine
connect(db='asc', username='ascUser', password='123')

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

"""
DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'assocam',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'postgres',
            'PASSWORD': 'radice',
            'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        },
}
"""


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'IT'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_PATH = os.path.join(BASE_DIR, 'static')


STATICFILES_DIRS = (
    STATIC_PATH,
)

#
# Qui invece salvo i file di cui faccio l'upload.
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = 'uploads/'

#
# E qui memorizzo i dati del mio filesystem.
SIFILEDATA_ROOT = os.path.join(BASE_DIR, 'data')
SIFILEDATA_URL = '/data/'

LOGIN_REDIRECT_URL = 'index'
