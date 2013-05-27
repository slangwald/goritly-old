from django.conf.urls import patterns,url,include
#from django.views.generic.simple import direct_to_template

import websites.views as views

urlpatterns = patterns('',
    url(r'^index$',views.index),
    url(r'^new$',views.new),
    url(r'^dashboard$',views.dashboard),
    url(r'^set_active_website/(\d+)?$',views.set_active_website),
    url(r'^filter',views.filter),
    #url(r'^mark',views.set_mark),
    url(r'^bubble',views.get_bubble_chart_json),
    #url(r'^line',views.get_line_chart_json),
    url(r'^set_metric',views.set_metric),
    url(r'^set_bar_options',views.set_options),
    url(r'^set_seperation',views.set_seperation),
    url(r'^bar',views.get_bar_chart_json),
    url(r'^sidebar',views.get_sidebar),
    url(r'^kpi',views.get_kpi_board),
    )
