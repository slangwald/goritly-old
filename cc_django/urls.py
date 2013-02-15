from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^websites/', include('websites.urls')),
    (r'^import/google_analytics/', include('data_import.google_analytics.urls')),
    (r'^import/spreadsheet/', include('data_import.spreadsheet.urls')),
    (r'^profiles/', include('profiles.urls')),
    url(r'^imprint', 'django.views.generic.simple.direct_to_template', {'template': 'imprint.html'},name = 'imprint'),
    url(r'^terms', 'django.views.generic.simple.direct_to_template', {'template': 'terms.html'},name = 'terms'),
    url(r'^data_protection', 'django.views.generic.simple.direct_to_template', {'template': 'data_protection.html'},name = 'data_protection'),
)
