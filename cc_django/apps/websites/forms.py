# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse,resolve
import django.core.validators as validators
from django.utils.translation import ugettext as _
import websites.models as models

class WebsiteForm(forms.Form):

    accepted_terms = forms.BooleanField()
    name = forms.CharField(max_length = 100)
    
