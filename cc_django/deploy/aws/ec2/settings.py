import boto

#General settings

REGION = 'eu-west-1'
AZ = 'eu-west-1a'

#Access keys

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

#Web server settings

WEB_SERVER_INSTANCE_TYPE = 't1.micro'
WEB_SERVER_INSTANCE_NAME = "django_web_server"
WEB_SERVER_SECURITY_GROUP = "webserver"
WEB_SERVER_KEY_PAIR = 'webserver'
WEB_SERVER_SSH_USER = "ubuntu"
WEB_SERVER_DJANGO_DIRECTORY = "/var/django"
WEB_SERVER_APP_DIRECTORY = "soma"
WEB_SERVER_REPOSITORY_URL = 'git@bitbucket.org:andreasdewes/conversion_cow_django.git'
