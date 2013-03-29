from django.conf.urls import patterns,url,include
#from django.views.generic.simple import direct_to_template

import websites.views as views

urlpatterns = patterns('',
    url(r'^index$',views.index),
    url(r'^new$',views.new),
    url(r'^dashboard$',views.dashboard),
    url(r'^set_active_website/(\d+)?$',views.set_active_website),
    )
