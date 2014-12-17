# -*- coding: utf-8 -*-

SECRET_KEY = 'a'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'canvas_api_token',
    'tests',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'tests.urls'

LTI_OAUTH_CREDENTIALS = {
    'test_consumer': 'test_consumer_secret'
}

LTI_APP_DEVELOPER_KEYS = {
    'test_consumer': {
        'client_id': 'test_client',
        'client_secret': 'test_client_secret'
    }
}
