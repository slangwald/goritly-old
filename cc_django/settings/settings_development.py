from settings_base import *

import os.path


EMAIL_ACTION_REPEAT_TIME = 20
EMAIL_INFO_FROM_ADDRESS = 'Andreas Dewes <andreas.dewes@gmail.com>'
EMAIL_USE_HTML = False
IGNORE_MISSING_BETA_KEY = True
CONFIRM_SIGNUP_BY_ADMIN = False

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'andreas.dewes@gmail.com'
EMAIL_HOST_PASSWORD = 'logtidaomtgiluut'

EMAIL_SERVER_URL = "http://192.168.150.200:8000"

DEVELOPMENT = True

DEBUG = True
TEMPLATE_DEBUG = True

import djcelery

"""
Settings for Celery.
"""
djcelery.setup_loader()

BROKER_URL = "amqp://cc_django:cc_django@localhost:5672/cc_django"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("profiles.mailer", )
CELERYD=PROJECT_PATH+"/../manage.py celeryd"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cc_test',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': { 'init_command': 'SET storage_engine=INNODB;' }
    }
}
