import os
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import data_import.spreadsheet.views as views

urlpatterns = patterns('',
    # Example:
    (r'^$', views.index),
)