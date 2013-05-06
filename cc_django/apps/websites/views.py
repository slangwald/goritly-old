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
import websites.models as models
import websites.forms as forms
from profiles.views import login_required
import utils.models as util_models

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
@csrf_exempt
def filter(request):
    """
    AJAX function is excluded from CSRF protection
    """
    request.session['filter-channel'] = []
    if('filter-channel' in request.POST):
        request.session['filter-channel'] = request.POST.getlist('filter-channel')
    
    request.session['filter-campaign'] = []    
    if('filter-campaign' in request.POST):
        request.session['filter-campaign'] = request.POST.getlist('filter-campaign')
    
    request.session['filter-partner'] = []    
    if('filter-partner' in request.POST):
        request.session['filter-partner1'] = request.POST.getlist('filter-partner')
    
    
    request.session['filter-date-from'] = ""
    request.session['filter-date-to']   = ""
    if('filter-date-from' in request.POST and 'filter-date-to' in request.POST):
        request.session['filter-date-from'] = request.POST['filter-date-from']
        request.session['filter-date-to']   = request.POST['filter-date-to']
    
    if 'model' in request.POST:
        request.session['model'] = request.POST['model']
    
    request.session.modified = True
    return HttpResponseRedirect('/websites/dashboard')

kpi_data = {}
def add_to_kpi(channel, key, value):
    if value == None:
        return

    if channel not in kpi_data:
        kpi_data[channel] = {
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
    kpi_data[channel][key] = float(value)

@login_required()
def get_kpi_board(request):
    model = request.session['model']
    session = request.session
    filter = ''
    if('filter-date-from' in session and 'filter-date-to' in session):
        filter += ' `date` BETWEEN "%s" AND "%s" ' % (session['filter-date-from'], session['filter-date-to'])
    if 'filter-campaign' in session:
        if len(session['filter-campaign']):
            if filter != "":
                filter += " AND "
            filter +=  ' campaign_id IN(%s) ' % (', '.join(str(int(v)) for v in session['filter-campaign']))
    if 'filter-channel' in session:
        if len(session['filter-channel']):
            if filter != "":
                filter += " AND "
            filter += ' channel_id IN(%s) ' % (', '.join(str(int(v)) for v in session['filter-channel']))
    
    if filter != "":
        filter = ' WHERE ' + filter
    
    #ROI
    sql = util_models.CustomerCLV.objects.raw("""
       SELECT id, channel_id, AVG(`""" + model + """`/cost)*100 as roi FROM utils_customerclv """ + filter + """ GROUP BY channel_id
    """)
    for line in sql:
        add_to_kpi(line.channel.name, 'roi', line.roi)
    
    #CLV (per customer)
    sql = util_models.CustomerCLV.objects.raw("""
        SELECT id, channel_id, SUM(`""" + model + """`)/count(DISTINCT `customer_id`) as clv_cust FROM utils_customerclv """ + filter + """ GROUP BY channel_id
    """)
    
    for line in sql:
        add_to_kpi(line.channel.name, 'clv_per_customer', line.clv_cust)
    
    #Number of Customers
    sql = util_models.CustomerCLV.objects.raw("""
        SELECT id, channel_id, count(DISTINCT `customer_id`) as customer_count FROM utils_customerclv """ + filter + """ GROUP BY channel_id
    """)
    channel_customer_count = {}
    for line in sql:
        add_to_kpi(line.channel.name, 'customer_count', line.customer_count)
        channel_customer_count[line.channel.name] = line.customer_count
    
    #Total CLV
    #Total CAC
    sql = util_models.CustomerCLV.objects.raw("""
        SELECT id, channel_id, SUM(`""" + model + """`) as total_clv, SUM(`cost`) as total_cost FROM utils_customerclv """ + filter + """ GROUP BY channel_id
    """)
    for line in sql:
        add_to_kpi(line.channel.name, 'clv_total', line.total_clv)
        add_to_kpi(line.channel.name, 'cac_total', line.total_cost)
        add_to_kpi(line.channel.name, 'cac_avg', line.total_cost/channel_customer_count[line.channel.name])
    
    # Total Revenue
    sql = util_models.Attributions.objects.raw("""
        SELECT id, channel_id, SUM(`""" + model + """`) as total_revenue FROM utils_attributions """ + filter + """ GROUP BY channel_id
    """)
    for line in sql:
        add_to_kpi(line.channel.name, 'revenue_total', line.total_revenue)
        add_to_kpi(line.channel.name, 'revenue_per_customer', (line.total_revenue/channel_customer_count[line.channel.name]))
    
    
    """
    MISSING:
    - CAC (ie cost of customer acquisition)
    """
    
    kpi_view = []
    for channel in kpi_data:
        kpi_view.append({
            'name'                     :          kpi_data[channel]['name'                   ],
            'roi'                      : "%.1f" % kpi_data[channel]['roi'                    ],
            'roi_change'               : "%.2f" % kpi_data[channel]['roi_change'             ],
            'clv_per_customer'         : "%.2f" % kpi_data[channel]['clv_per_customer'       ],
            'clv_per_customer_change'  : "%.2f" % kpi_data[channel]['clv_per_customer_change'],
            'customer_count'           : "%.0f" % kpi_data[channel]['customer_count'         ],
            'customer_count_change'    : "%.2f" % kpi_data[channel]['customer_count_change'  ],
            'clv_total'                : "%.2f" % kpi_data[channel]['clv_total'              ],
            'clv_total_change'         : "%.2f" % kpi_data[channel]['clv_total_change'       ],
            'cac_total'                : "%.2f" % kpi_data[channel]['cac_total'              ],
            'cac_total_change'         : "%.2f" % kpi_data[channel]['cac_total_change'       ],
            'revenue_total'            : "%.2f" % kpi_data[channel]['revenue_total'          ],
            'revenue_total_change'     : "%.2f" % kpi_data[channel]['revenue_total_change'   ],
            'revenue_per_customer'     : "%.2f" % kpi_data[channel]['revenue_per_customer'   ],
            'revenue_per_customer_change': "%.2f" % kpi_data[channel]['revenue_per_customer_change'],
            'cac_avg': "%.2f" % kpi_data[channel]['cac_avg'],
            
        })
        
    
    return render_to_response('websites/kpi.html', {'kpis': kpi_view})

@login_required()
def get_sidebar(request):
    if 'model' not in request.session:
        request.session['model'] = 'linear'
    
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
        
    filter = {}
    if 'filter-channel' in request.session:
        filter['channel'] = request.session['filter-channel']
    if 'filter-campaign' in request.session:
        filter['campaign'] = request.session['filter-campaign']
    if 'filter-partner' in request.session:
        filter['partner'] = request.session['filter-partner']
    if('filter-date-from' in request.session and 'filter-date-to' in request.session):
        filter['from'] = request.session['filter-date-from']
        filter['to'] = request.session['filter-date-to']
    
    if 'model' in request.session:
        filter['model'] = request.session['model']
    
    models = get_models_available()
    
    return render_to_response('websites/filter.html', {'request'    : request,
                                                       'filter'     : filter,
                                                       'channels'   : channels, 
                                                       'campaigns'  : campaigns, 
                                                       'partners'   : partners,
                                                       'models_available': models
                                                      })


@login_required()
def dashboard(request):
    context = RequestContext(request,{})
    return render_to_response('websites/dashboard.html', {'request'    : request,
                                                          'context'    : context, 
                                                          })

def get_models_available():
    models = [
              {'id': 'linear'     , 'label': 'Linear'                },
              {'id': 'u_shape'    , 'label': 'U-Shape (40-20-40)'    },
              {'id': 'first_click', 'label': 'First Click'           },
              {'id': 'last_click' , 'label': 'Last Click'            },
              {'id': 'decay'      , 'label': 'exponential/time Decay'}
             ]
    
    return models
    

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
    session = request.session
    
    filter = ''
    
    if('filter-date-from' in session and 'filter-date-to' in session):
        filter += ' `first_ordered_at` BETWEEN "%s" AND "%s" ' % (session['filter-date-from'], session['filter-date-to'])
    
    
    if 'filter-campaign' in session:
        if len(session['filter-campaign']):
            if filter != "":
                filter += " AND "
            filter +=  ' campaign_id IN(%s) ' % (', '.join(str(int(v)) for v in session['filter-campaign']))
    if 'filter-channel' in session:
        if len(session['filter-channel']):
            if filter != "":
                filter += " AND "
            filter += ' channel_id IN(%s) ' % (', '.join(str(int(v)) for v in session['filter-channel']))
    if 'filter-partner' in session:
        if len(session['filter-partner']):
            if filter != "":
                filter += " AND "
            filter += ' partner_id IN(%s) ' % (', '.join(str(int(v)) for v in session['filter-partner']))
    
    
    if filter != "":
        filter = ' WHERE ' + filter
    
    model = session['model']
    bar_data = util_models.CustomerCLV.objects.raw('SELECT id, `first_ordered_at` as `date`, AVG(`' + model + '`) as sum_linear, channel_id FROM utils_customerclv ' + filter + ' GROUP BY `first_ordered_at`, channel_id ORDER BY `date` DESC')
    by_channel = {}
    bar_chart = []
    dates_available = {}
    

    for bar in bar_data:
        date = int(bar.date.strftime('%s000'))
        if not date in dates_available:
            dates_available[date] = date
    
    for bar in bar_data:
        date = int(bar.date.strftime('%s000'))
        if not bar.channel.name in by_channel:
            by_channel[bar.channel.name] = {}
            for date_check in dates_available:
                by_channel[bar.channel.name][date_check] = {
                                                      'x': date_check,
                                                      'y': 0
                                                      }
        
        by_channel[bar.channel.name][date] = {
             'x': date,
             'y': float(bar.sum_linear),
             }
    by_channel_clean = {}
    for channel in by_channel:
        for date in by_channel[channel]:
            if not channel in by_channel_clean:
                by_channel_clean[channel] = []
                
            by_channel_clean[channel].append(by_channel[channel][date])
    
    for channel in by_channel_clean:
        bar_chart.append({
            'key': channel,
            'values': by_channel_clean[channel]
        })
        
    return HttpResponse(json.dumps(bar_chart), content_type="application/json")


@login_required()
def get_line_chart_json(request):
    session = request.session
    filter = ''
    if('filter-date-from' in session and 'filter-date-to' in session):
        filter += ' AND `date` BETWEEN "%s" AND "%s" ' % (session['filter-date-from'], session['filter-date-to'])
    if 'filter-campaign' in session:
        if len(session['filter-campaign']):
            filter +=  ' AND campaign_id IN(%s) ' % (', '.join(str(int(v)) for v in session['filter-campaign']))
    if 'filter-channel' in session:
        if len(session['filter-channel']):
            filter += ' AND channel_id IN(%s) ' % (', '.join(str(int(v)) for v in session['filter-channel']))
    if 'filter-partner' in session:
        if len(session['filter-partner']):
            filter += ' AND partner_id IN(%s) ' % (', '.join(str(int(v)) for v in session['filter-partner']))
    
    model = session['model']
    line_data = util_models.CustomerCLV.objects.raw('select `id`, `date`, AVG(`days`) as avg_days ,`channel_id` FROM utils_customerclv WHERE (`' + model + '`/`cost` * 100) BETWEEN 100 AND 125 ' + filter + ' GROUP BY `date` ORDER BY `date`')
    
    values = []
    for line in line_data:
        date = str(line.date)
        values.append({
           'x': int(line.date.strftime('%s000')),
           'y': float(line.avg_days)
        })
        
    line_chart = [{
        'key': 'days to reach 100% ROI',
        'values': values
    }]
    return HttpResponse(json.dumps(line_chart), content_type="application/json")
@login_required()
def get_bubble_chart_json(request):
    session = request.session
    filter = ''
    
    if('filter-date-from' in session and 'filter-date-to' in session):
        filter += ' `date` BETWEEN "%s" AND "%s" ' % (session['filter-date-from'], session['filter-date-to'])
    
    if 'filter-campaign' in session:
        if len(session['filter-campaign']):
            if filter != "":
                filter += " AND "
            filter +=  ' campaign_id IN(%s) ' % (', '.join(str(int(v)) for v in session['filter-campaign']))
    if 'filter-channel' in session:
        if len(session['filter-channel']):
            if filter != "":
                filter += " AND "
            filter += ' channel_id IN(%s) ' % (', '.join(str(int(v)) for v in session['filter-channel']))
    
    if 'filter-partner' in session:
        if len(session['filter-partner']):
            if filter != "":
                filter += " AND "
            filter += ' partner_id IN(%s) ' % (', '.join(str(int(v)) for v in session['filter-partner']))
    
    if filter != "":
        filter = ' WHERE ' + filter
    
    
    
    model = session['model']
    bubble_data = util_models.Attributions.objects.raw('SELECT *, SUM(cost) as sum_cost, SUM(`' + model + '`) as sum_linear, SUM(orders) as sum_orders FROM utils_attributions ' + filter + ' GROUP BY channel_id')
    
    bubble_chart = []
    by_channel = {}
    for bubble in bubble_data:
        if not bubble.channel.name in by_channel:
            by_channel[bubble.channel.name] = []
        
        realcost = float(bubble.sum_cost) / float(bubble.sum_orders)
        reallinear = float(bubble.sum_linear) / float(bubble.sum_orders)
        by_channel[bubble.channel.name].append(
            {
             'x': realcost,
             'y': reallinear,
             'size': int(bubble.orders)
             }
        )
    for channel in by_channel:
        bubble_chart.append({
            'key': channel,
            'values': by_channel[channel]
        })
        
    
    return HttpResponse(json.dumps(bubble_chart), content_type="application/json")

@login_required()
def set_active_website(request,website_id = None):
    if not website_id:
        request.session['active_website_id'] = None
        return redirect(reverse("websites.views.index"))
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
