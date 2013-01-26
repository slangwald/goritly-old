from settings_base import *

import os.path

EMAIL_ACTION_REPEAT_TIME = 20
EMAIL_INFO_FROM_ADDRESS = 'Conversion Cow <moo@conversion-cow.com>'
EMAIL_USE_HTML = False
IGNORE_MISSING_BETA_KEY = True
CONFIRM_SIGNUP_BY_ADMIN = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

EMAIL_SERVER_URL = "http://192.168.150.200:8000"

DEVELOPMENT = False

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cc_django_production',                      # Or path to database file if using sqlite3.
        'USER': 'cc_django',                      # Not used with sqlite3.
        'PASSWORD': 'cc_django',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
