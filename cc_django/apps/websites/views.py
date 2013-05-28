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
from django.views.decorators.csrf import csrf_protect, csrf_exempt
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

from django.core.cache import cache

from django.core import serializers

import logging

import global_settings
import websites.models as wmodels
import websites.forms as forms
from profiles.views import login_required
import utils.models as util_models
from websites.metrics import * 
from django.core import serializers


import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')


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
"""
------------------------
FILTERS 
------------------------
"""

FILTERS_AVAILABLE = [
      'partner' 
    , 'channel' 
    , 'campaign'
    , 'date'
    , 'model'   
]

def set_filter(request):
    request.session['filter'] = {}
    
    if('filter-channel' in request.POST):
        request.session['filter']['channel'] = request.POST.getlist('filter-channel')
    
    if('filter-campaign' in request.POST):
        request.session['filter']['campaign'] = request.POST.getlist('filter-campaign')
    
    if('filter-partner' in request.POST):
        request.session['filter']['partner'] = request.POST.getlist('filter-partner')
    
    if('filter-date-from' in request.POST and 'filter-date-to' in request.POST):
        request.session['filter']['date'] = {}
        request.session['filter']['date']['from'] = request.POST['filter-date-from']
        request.session['filter']['date']['to']   = request.POST['filter-date-to']
    
    if 'model' in request.POST:
        request.session['model'] = request.POST['model']
    
    request.session.modified = True
    return True

def init_filters():
    filters = {}
    
    for filter in FILTERS_AVAILABLE:
        filters[filter] = None
    return filters

def get_filter(request):
    filters = init_filters()
    
    if not 'filter' in request.session:
        return filters
    
    for filter in request.session['filter']:
        filters[filter] = request.session['filter'][filter]
        
    filters['model'] = request.session['model']
    
    return filters

"""
------------------------
VIEWS 
------------------------
"""
@login_required()
def index(request):
    context = RequestContext(request,{})
    return render_to_response('websites/index.html',context)

@login_required()
@csrf_exempt
def filter(request):
    """
    AJAX function is excluded from CSRF protection
    """
    set_filter(request)
    print request.session['filter']
    return HttpResponse('')

class KpiBoard():
    def __init__(self):
        self.kpi_data = {}
    
    def add_to_kpi(self, channel, key, value):
        if value == None:
            return
        if channel not in self.kpi_data:
            self.kpi_data[channel] = {
                'name': channel,
                'roi': 0,
                'roi_change': 0,
                'clv_per_customer': 0,
                'clv_per_customer_change': 0,
                'customer_count': 0,
                'customer_count_change': 0,
                'clv_total': 0,
                'clv_total_change': 0,
                'cac_total': 0,
                'cac_total_change': 0,
                'revenue_total': 0,
                'revenue_total_change': 0,
                'revenue_per_customer': 0,
                'revenue_per_customer_change': 0,
                'cac_avg': 0,
            }
        self.kpi_data[channel][key] = float(value)

@login_required()
def get_kpi_board(request):
    session = request.session
    
    kpi_model = KpiBoard()
    
    
    for metric in METRICS:
        constructor_right = METRICS[metric]['class']
        options_right     = METRICS[metric]['options']
        label_right       = METRICS[metric]['label']
        options_right['timerange'] = request.session['timerange']
        options_right['kpi_view'] = True
        metric_right = constructor_right(
            model      = request.session['model'],
            filter     = get_filter(request), 
            options    = options_right,
            seperation = request.session['kpi-seperation']
        )
        lines = metric_right.get_data_kpi()
        
        for line in lines:
            if request.session['kpi-seperation'] == 'aggregated':
                channel = 'All'
            else:
                channel = getattr(line, request.session['kpi-seperation']).name
            kpi_model.add_to_kpi(channel, metric, line.value)
        
    
    print kpi_model.kpi_data
    
    
    kpi_view = []
    for channel in kpi_model.kpi_data:
        kpi_view.append({
            'name'                       : kpi_model.kpi_data[channel]['name'                       ],
            'roi'                        : locale.format('%.1f', kpi_model.kpi_data[channel]['roi'                        ], grouping=True),
            #'roi_change'                 : locale.format('%d', kpi_model.kpi_data[channel]['roi_change'                 ], grouping=True),
            'clv_per_customer'           : '$' + locale.format('%.2f', kpi_model.kpi_data[channel]['clv'                        ], grouping=True),
            #'clv_per_customer_change'    : locale.format('%d', kpi_model.kpi_data[channel]['clv_per_customer_change'    ], grouping=True),
            'customer_count'             : locale.format('%d', kpi_model.kpi_data[channel]['customer_count'             ], grouping=True),
            #'customer_count_change'      : locale.format('%d', kpi_model.kpi_data[channel]['customer_count_change'      ], grouping=True),
            'clv_total'                  : '$' + locale.format('%d', kpi_model.kpi_data[channel]['customer_equity'            ], grouping=True),
            #'clv_total_change'           : locale.format('%d', kpi_model.kpi_data[channel]['clv_total_change'           ], grouping=True),
            'cac_total'                  : '$' + locale.format('%d', kpi_model.kpi_data[channel]['marketingspend'             ], grouping=True),
            #'cac_total_change'           : locale.format('%d', kpi_model.kpi_data[channel]['cac_total_change'           ], grouping=True),
            'revenue_total'              : '$' + locale.format('%d', kpi_model.kpi_data[channel]['revenue_total'              ], grouping=True),
            #'revenue_total_change'       : locale.format('%d', kpi_model.kpi_data[channel]['revenue_total_change'       ], grouping=True),
            'revenue_per_customer'       : '$' + locale.format('%.2f', kpi_model.kpi_data[channel]['revenue_per_customer'       ], grouping=True),
            #'revenue_per_customer_change': locale.format('%d', kpi_model.kpi_data[channel]['revenue_per_customer_change'], grouping=True),
            'cac_avg'                    : '$' + locale.format('%.2f', kpi_model.kpi_data[channel]['cac'                        ], grouping=True),
            'profit_per_customer'       : '$' + locale.format('%.2f', kpi_model.kpi_data[channel]['profit_per_customer'] /kpi_model.kpi_data[channel]['customer_count'] , grouping=True),
        })
        
    return render_to_response('websites/kpi.html', {'kpis': kpi_view})



@login_required()
def get_sidebar(request):
    
    channels  = cache.get('channels')
    if not channels:
        channels = get_channels()
        cache.set('channels', channels, 3600)
    
    
    campaigns = cache.get('campaigns')
    if not campaigns:
        campaigns = get_campaigns()
        cache.set('campaigns', campaigns, 3600)
    
    partners  = cache.get('partners')
    if not partners:
        partners = get_partners()
        cache.set('partners', partners, 3600)
        
    return render_to_response('websites/filter.html', {
        'request'          : request,
        'filter'           : get_filter(request),
        'channels'         : channels, 
        'campaigns'        : campaigns, 
        'partners'         : partners,
        'models_available' : get_models_available()
    })


TIMERANGE_UNITS = ['today', 'days', 'weeks', 'months']

@login_required()
def dashboard(request):
    context = RequestContext(request,{})
    
    set_session_defaults(request)
    
    return render_to_response('websites/dashboard.html', {
          'request': request
        , 'context': context
        , 'marks'  : get_marks()
        , 'filter' : get_filter(request)
        , 'metrics': get_view_metrics()
        , 'selected_metrics': {
            'right': request.session['omni-metric-right'], 
            'left' : request.session['omni-metric-left']
        }
        , 'selected_bubble_metrics': {
            'right': request.session['bubble-metric-right'], 
            'left' : request.session['bubble-metric-left'],
            'size' : request.session['bubble-metric-size']
        }
        , 'seperations': {
            'kpi'   : request.session['kpi-seperation'],
            'omni'  : request.session['omni-seperation'],
            'bubble': request.session['bubble-seperation']
        }
        , 'timeunits': TIMERANGE_UNITS
    })

@login_required()
@csrf_exempt
def set_options(request):
    if 'timerange-unit' in request.POST and 'timerange-value' in request.POST:
        unit = request.POST['timerange-unit']
        value = request.POST['timerange-value']
        days = None
        if unit == 'days':
            days = value
        if unit == 'weeks':
            days = value * 7
        if unit == 'months':
            days = value * 30
        request.session['timerange'] = days
        
    return HttpResponse('', )

@login_required()
@csrf_exempt
def set_metric(request):
    post = request.POST
    if 'omni-metric-left' in post:
        request.session['omni-metric-left'] = post['omni-metric-left']
    
    if 'omni-metric-right' in post:
        request.session['omni-metric-right'] = post['omni-metric-right']
    
    if 'bubble-metric-left' in post:
        request.session['bubble-metric-left'] = post['bubble-metric-left']
    
    if 'bubble-metric-right' in post:
        request.session['bubble-metric-right'] = post['bubble-metric-right']
    
    if 'bubble-metric-size' in post:
        request.session['bubble-metric-size'] = post['bubble-metric-size']
        
    return HttpResponse('', )

@login_required()
@csrf_exempt
def set_seperation(request):
    
    if 'omni-seperation' in request.POST:
        request.session['omni-seperation'] = request.POST['omni-seperation']
    
    if 'kpi-seperation' in request.POST:
        request.session['kpi-seperation'] = request.POST['kpi-seperation']
    
    if 'bubble-seperation' in request.POST:
        request.session['bubble-seperation'] = request.POST['bubble-seperation']
    
    
    return HttpResponse('', )

def set_session_defaults(request):
    
    if not 'omni-metric-right' in request.session:
        request.session['omni-metric-right'] = 'cac'
    
    if not 'omni-metric-left' in request.session:
        request.session['omni-metric-left'] = 'roi'
        
    if not 'bubble-metric-right' in request.session:
        request.session['bubble-metric-right'] = 'cac'
    
    if not 'bubble-metric-left' in request.session:
        request.session['bubble-metric-left'] = 'roi'
    
    if not 'bubble-metric-size' in request.session:
        request.session['bubble-metric-size'] = 'roi'
    
    if not 'model' in request.session:
        request.session['model'] = 'linear'
    
    if not 'filter' in request.session:
        request.session['filter'] = {}
    
    if not 'omni-seperation' in request.session:
        request.session['omni-seperation'] = 'aggregated'
    if not 'bubble-seperation' in request.session:
        request.session['bubble-seperation'] = 'partner'
    if not 'kpi-seperation' in request.session:
        request.session['kpi-seperation'] = 'aggregated'
    
    if not 'timerange' in request.session:
        request.session['timerange'] = None
    
    if not 'date' in request.session['filter']:
        edge_dates = get_first_and_last_date()
        request.session['filter']['date'] = {}
        request.session['filter']['date']['from'] = edge_dates['first'].strftime('%Y-%m-%d')
        request.session['filter']['date']['to']   = edge_dates['last'].strftime('%Y-%m-%d')

    if not 'mark' in request.session:
        request.session['mark'] = 100

def get_view_metrics():
    view_metrics = []
    for metric in METRICS:
        view_metric = METRICS[metric].copy()
        view_metric['id'] = metric
        view_metrics.append(view_metric)
    
    return view_metrics
    

def get_first_and_last_date():
    first = util_models.CustomerCLV.objects.order_by('date')[0]
    last = util_models.CustomerCLV.objects.order_by('-date')[0]
    return {'first': first.date, 'last': last.date}
    
    

def get_models_available():
    models = [
        {'id': 'linear'     , 'label': 'Linear'            },
        {'id': 'u_shape'    , 'label': 'U-Shape (40-20-40)'},
        {'id': 'first_click', 'label': 'First Click'       },
        {'id': 'last_click' , 'label': 'Last Click'        },
        {'id': 'decay'      , 'label': 'Time Decay'        }
    ]
    
    return models
    
def get_marks():
    marks = [25, 50, 75, 100, 125, 150, 175, 200, 300, 400, 500]
    return marks

def get_partners():
    partners = map(lambda p: {'id': str(p.id), 'name': p.name}, util_models.Partner.objects.all())
    return partners

def get_campaigns():
    campaigns = map(lambda c: {'id': str(c.id), 'name': c.name}, util_models.Campaign.objects.all())
    return campaigns

def get_channels():
    channels = map(lambda c: {'id': str(c.id), 'name': c.name}, util_models.Channel.objects.all())
    return channels

@login_required()
def get_bar_chart_json(request):
    
    constructor_right = METRICS[request.session['omni-metric-right']]['class']
    constructor_left  = METRICS[request.session['omni-metric-left' ]]['class']

    options_right     = METRICS[request.session['omni-metric-right']]['options']
    options_left      = METRICS[request.session['omni-metric-left' ]]['options']

    label_right       = METRICS[request.session['omni-metric-right']]['label']
    label_left        = METRICS[request.session['omni-metric-left' ]]['label']
    
    options_right['timerange'] = request.session['timerange']
    options_left['timerange']  = request.session['timerange']
    
    options_right['kpi_view'] = False
    options_left['kpi_view'] = False
    
    metric_right = constructor_right(
        model      = request.session['model'],
        filter     = get_filter(request), 
        options    = options_right,
        seperation = request.session['omni-seperation']
    )
    
    metric_left = constructor_left(
        model      = request.session['model'],
        filter     = get_filter(request), 
        options    = options_left,
        seperation = request.session['omni-seperation']
    )
    
    if request.session['omni-seperation'] == "aggregated":
        json = """
        [{
            "key"    : " """ + label_left + """ " ,
            "bar"    : true,
            "values" : """ + metric_left.get_json() + """
        },{
            "key"    : " """ + label_right + """ " ,
            "values" : """ + metric_right.get_json() + """
        }]
        """
    else:
        json = metric_left.get_json()
        
    return HttpResponse(json, content_type="application/json")

@login_required()
def get_bubble_chart_json(request):
    constructor_bottom = METRICS[request.session['bubble-metric-right']]['class']
    constructor_left   = METRICS[request.session['bubble-metric-left' ]]['class']
    constructor_size   = METRICS[request.session['bubble-metric-size' ]]['class']
    
    options_bottom     = METRICS[request.session['bubble-metric-right']]['options']
    options_left       = METRICS[request.session['bubble-metric-left' ]]['options']
    options_size       = METRICS[request.session['bubble-metric-size' ]]['options']
    
    label_bottom       = METRICS[request.session['bubble-metric-right']]['label']
    label_left         = METRICS[request.session['bubble-metric-left' ]]['label']
    label_size         = METRICS[request.session['bubble-metric-size' ]]['label']
    
    #options_bottom['timerange'] = request.session['timerange']
    #options_left['timerange']   = request.session['timerange']
    
    metric_bottom = constructor_bottom(
        model      = request.session['model'],
        filter     = get_filter(request), 
        options    = options_bottom,
        seperation = request.session['bubble-seperation']
    )
    
    metric_left = constructor_left(
        model      = request.session['model'],
        filter     = get_filter(request), 
        options    = options_left,
        seperation = request.session['bubble-seperation']
    )
    
    metric_size = constructor_size(
        model      = request.session['model'],
        filter     = get_filter(request), 
        options    = options_size,
        seperation = request.session['bubble-seperation']
    )
    
    seperator = request.session['bubble-seperation']
    
    bla = {'y': metric_left.get_data_bubble(), 
           'x': metric_bottom.get_data_bubble(), 
           'size': metric_size.get_data_bubble()}
    
    add_krams = {}
    
    for position in bla:
        for line in bla[position]:
            key_attr = getattr(line, seperator).name
            if not key_attr in add_krams:
                add_krams[key_attr] = {}
            add_krams[key_attr][position] = line.value
    
    _json = []
    for bubble in add_krams:
        _json.append({
            "key"    : bubble,
            "values" : [add_krams[bubble]]
        })
    return HttpResponse(json.dumps(_json), content_type="application/json")
    
    
    

@login_required()
def set_active_website(request,website_id = None):
    if not website_id:
        request.session['active_website_id'] = None
        return redirect(reverse("websites.views.index"))
    try:
        website = wmodels.Website.objects.get(id = website_id)
    except wmodels.Website.DoesNotExist:
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
            website = wmodels.Website(name = data['name'])
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
