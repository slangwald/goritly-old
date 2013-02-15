import os
import logging
import httplib2
import datetime

from profiles.views import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,redirect
from django.template import Context, loader, RequestContext
import storage

@login_required()
def index(request):
    gridStorage = storage.GridFSStorage

@login_required()
def upload_file(request):
    pass