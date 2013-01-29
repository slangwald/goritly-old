import os
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import google_analytics.views as views

urlpatterns = patterns('',
    # Example:
    (r'^$', views.index),
    (r'^auth_return', views.auth_return),
)