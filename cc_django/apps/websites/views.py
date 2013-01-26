# Create your views here.
# -*- coding: utf-8 -*-
from functools import wraps
import urllib
import traceback
import datetime
import random
import os.path
import re
import json
import copy
import PIL.Image

from django.template import Context, loader, RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response,redirect
from django.core.urlresolvers import reverse,resolve
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as dlogin
from django.contrib.auth import logout as dlogout
from django.db import IntegrityError
from django.http import Http404
from django.core.exceptions import PermissionDenied

import global_settings
import websites.models as models
import websites.forms as forms
from profiles.views import login_required

class valid_website_required(object):

    def __call__(self,function):

        @wraps(function)
        def check_for_valid_website(request,*args,**kwargs):
            if not hasattr(request,'active_website'):
                raise PermissionDenied
            if not request.user.is_authenticated() or not ( request.user in request.active_website.owners.all() or request.user in request.active_website.admins.all() ) and not request.user.is_staff:
                raise PermissionDenied
            return function(request,*args,**kwargs)
        
        return check_for_valid_website


@login_required()
def index(request):
    context = RequestContext(request,{})
    return render_to_response('websites/index.html',context)

@login_required()
def dashboard(request):
    context = RequestContext(request,{})
    return render_to_response('websites/dashboard.html',context)

@login_required()
def set_active_website(request,website_id = None):
    if not website_id:
        request.session['active_website_id'] = None
        return redirect(reverse("user_dashboards.views.index"))
    try:
        website = models.Website.objects.get(id = website_id)
    except models.Website.DoesNotExist:
        raise Http404
    if not request.user in website.owners.all() and not request.user in website.admins.all() and not request.user.is_staff:
        raise PermissionDenied
    request.session['active_website_id'] = website.id
    return redirect(dashboard)

@login_required()
def new(request):
    if request.method == 'POST':
        form = forms.WebsiteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            website = models.Website(name = data['name'])
            website.save()
            website.owners.add(request.user)
            request.flash["notice"] = _(u"Your website account has been created.")
            return redirect(index)
        else:
            request.flash.now["error"] = _(u"Please correct the indicated errors.")
    else:
        form = forms.WebsiteForm()
    context = RequestContext(request,{'form':form})
    return render_to_response('websites/new.html',context)
