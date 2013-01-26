# -*- coding: utf-8 -*-
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response,redirect
from django.utils.translation import ugettext as _
import re

def ask_question(request,**kwargs):
	return render_to_response('utils/question.html',RequestContext(request,kwargs))
