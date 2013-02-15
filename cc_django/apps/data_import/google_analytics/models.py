import pickle
import base64

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField

from websites.models import Website

class CredentialsModel(models.Model):
  website = models.ForeignKey(Website, unique = True)
  credential = CredentialsField()

class CredentialsAdmin(admin.ModelAdmin):
    pass

#admin.site.register(CredentialsModel, CredentialsAdmin)