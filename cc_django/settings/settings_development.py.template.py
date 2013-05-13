from settings_base import *

import os.path


EMAIL_ACTION_REPEAT_TIME = 20
EMAIL_INFO_FROM_ADDRESS = '%EMAIL_INFO_FROM_ADDRESS%'
EMAIL_USE_HTML = False
IGNORE_MISSING_BETA_KEY = True
CONFIRM_SIGNUP_BY_ADMIN = False

EMAIL_HOST = '%EMAIL_HOST%'
EMAIL_PORT = %EMAIL_PORT%
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '%EMAIL_USER%'
EMAIL_HOST_PASSWORD = '%EMAIL_PASSWORD%'

# eg http://192.168.150.200:8000
EMAIL_SERVER_URL = "%EMAIL_SERVER%"

DEVELOPMENT = True

DEBUG = True
TEMPLATE_DEBUG = True

import djcelery

"""
Settings for Celery.
"""
djcelery.setup_loader()

# amqp://cc_django:cc_django@localhost:5672/cc_django
BROKER_URL = "%CELERY_BROKER_URL%"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("profiles.mailer", )
CELERYD=PROJECT_PATH+"/../manage.py celeryd"

DATABASES = {
    %DATABASES%
}

#from django.db import connections
DATABASE_ROUTERS = ['cc_django.apps.utils.db_switch.UserDBRouter']
