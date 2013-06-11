import sys, os
import argparse
import math

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../.."))

import logging



import cc_django.settings as settings
from django.core.management import setup_environ

setup_environ(settings)

from utils.models import *
import pprint

from django import db

class CustomerProcessor():
    
    marks  = [
        25, 
        50, 
        75, 
        100, 
        125, 
        150, 
        175, 
        200, 
        300, 
        400, 
        500
    ]
    
    models = [
        'linear',
        'first_click',
        'last_click',  
        'decay',
        'u_shape'
    ]
    
    init_dict = {
        'linear': 0.00, 
        'first_click': 0.00, 
        'last_click': 0.00, 
        'decay': 0.00,
        'u_shape': 0.00,
        'cost': 0.00
    }
    
    def __init__(self, customer):
        """
        __INIT__ stuff
        """
        self.customer_attributions  = {}
        self.customer               = customer
        self.channel_attributions   = {}
        self.joined                 = None
        self.channel_attr_per_order = {}
        
        self.revenue_attributions   = {}
        self.revenue_attr_per_order = {}
        
        self.order_counter          = 0
    
    def add_campaign_numbers(self, type, partner, channel, campaign, value):
        """
        Adds different ROI marks to the customer_attribution
        """
        channel  = int(channel) 
        campaign = int(campaign)
        partner  = int(partner)
        
        key = (partner, channel, campaign)

        self.init_channel_attr_per_order(key)
        
        if not key in self.channel_attributions:
            self.channel_attributions[key] = self.init_dict.copy()
            
        self.channel_attributions[key][type] += value
        self.channel_attr_per_order[self.order_counter][key][type] += value
    
    def add_revenue_numbers(self, type, partner, channel, campaign, value):
        """
        Adds different ROI marks to the customer_attribution
        """
        channel  = int(channel) 
        campaign = int(campaign)
        partner  = int(partner)
        
        key = (partner, channel, campaign)

        self.init_revenue_attr_per_order(key)
        
        if not key in self.revenue_attributions:
            self.revenue_attributions[key] = self.init_dict.copy()
            
        self.revenue_attributions[key][type] += value
        self.revenue_attr_per_order[self.order_counter][key][type] += value
    
    def init_revenue_attr_per_order(self, key):
        if not self.order_counter in self.revenue_attr_per_order:
            self.revenue_attr_per_order[self.order_counter] = {}
            for key2 in self.revenue_attributions:
                if not key2 in self.revenue_attr_per_order[self.order_counter]:
                    self.revenue_attr_per_order[self.order_counter][key2] = self.init_dict.copy()
        
        if not key in self.revenue_attr_per_order[self.order_counter]:
            self.revenue_attr_per_order[self.order_counter][key] = self.init_dict.copy()
    
    def init_channel_attr_per_order(self, key):
        if not self.order_counter in self.channel_attr_per_order:
            self.channel_attr_per_order[self.order_counter] = {}
            for key2 in self.channel_attributions:
                if not key2 in self.channel_attr_per_order[self.order_counter]:
                    self.channel_attr_per_order[self.order_counter][key2] = self.init_dict.copy()
        
        if not key in self.channel_attr_per_order[self.order_counter]:
            self.channel_attr_per_order[self.order_counter][key] = self.init_dict.copy()
            
    
    def init_roi_marks(self, key):
        if not key in self.customer_attributions:
            self.customer_attributions[key] = {}
            for _model in self.models:
                self.customer_attributions[key][_model] = {}
                for _mark in self.marks:
                    self.customer_attributions[key][_model][_mark] = None
                    
    
    def add_roi_mark(self, partner, channel, campaign, model, mark, days):
        """
        Adds different ROI marks to the customer_attribution
        """
        channel  = int(channel) 
        campaign = int(campaign)
        key      = (partner, channel, campaign)
        
        self.init_roi_marks(key)
        
        if self.customer_attributions[key][model][mark] == None:
            self.customer_attributions[key][model][mark] = days
        if self.customer.id == 224:
            print 'add_roi_mark: mark:%s, model:%s, days:%s ' % (mark, model, self.customer_attributions[key][model][mark])
            
    def save_roi_marks(self):
        cm_entries = []
        for (partner, channel, campaign) in self.customer_attributions:
            
            key = (partner, channel, campaign)
            cm  = CustomerRoiMarks()
            
            roi_marks = {}
            for model in self.customer_attributions[key]:
                for mark in self.customer_attributions[key][model]:
                    setattr(cm, 'roi_%s_%s' % (model, mark), self.customer_attributions[key][model][mark])
            
            cm.channel_id  = channel  
            cm.campaign_id = campaign 
            cm.partner_id  = partner
            cm.customer    = self.customer 
            cm.joined      = self.joined
            
            #cm_entries.append(cm)
            
        #CustomerRoiMarks.objects.bulk_create(cm_entries)
    
    def start(self):
        
        cust_clv_entries = []
        
        customer = self.customer
        
        orders = customer.orders().order_by('ordered_at')
        clv = 0
        marketing_cost = 0
        
        if(len(orders)):
            print "customer:%s" % (customer.id)
            first_ordered_at = None
            iindex = -1
            for order in orders:
                self.order_counter += 1
                iindex += 1
                next_iindex = iindex+1
                
                print "customer:%s ordercounter:%s/%s" % (customer.id, self.order_counter, len(orders))
                if not first_ordered_at:
                    first_ordered_at = order.ordered_at
                    self.joined = first_ordered_at
                
                order_products = OrderProducts.objects.filter(order_id=order.id)
                costs_product = sum(map(lambda op: op.cost_per_unit * op.qty, order_products))
                # costs_returns
                order.value = order.revenue - (costs_product)
                #order.value = order.revenue
                order.save()
                clv               += order.value
                
                clicks = order.clicks()
                if(len(clicks)):
                    last_click_channel = clicks[len(clicks)-1].channel.id
                    last_click_campaign = clicks[len(clicks)-1].campaign.id
                    last_click_partner = clicks[len(clicks)-1].partner.id
                    self.add_campaign_numbers('last_click', last_click_partner, last_click_channel, last_click_campaign, order.value)
                    
                    
                    first_click_channel = clicks[0].channel.id
                    first_click_campaign = clicks[0].campaign.id
                    first_click_partner = clicks[0].partner.id
                    self.add_campaign_numbers(
                        'first_click', 
                        first_click_partner,
                        first_click_channel, 
                        first_click_campaign, 
                        order.value
                    )
    
                    if(len(clicks) == 2):
                        self.add_campaign_numbers('u_shape', clicks[0].partner.id, clicks[0].channel.id, clicks[0].campaign.id, order.value * 0.5)
                        self.add_campaign_numbers('u_shape', clicks[1].partner.id, clicks[1].channel.id, clicks[1].campaign.id, order.value * 0.5)
                    if(len(clicks) == 1):
                        self.add_campaign_numbers('u_shape', clicks[0].partner.id, clicks[0].channel.id, clicks[0].campaign.id, order.value)
                    if(len(clicks) > 2):
                        self.add_campaign_numbers('u_shape', clicks[0].partner.id, clicks[0].channel.id, clicks[0].campaign.id, order.value * 0.4)
                        self.add_campaign_numbers('u_shape', clicks[len(clicks)-1].partner.id, clicks[len(clicks)-1].channel.id, clicks[len(clicks)-1].campaign.id, order.value * 0.4)
                        for i in range(1, len(clicks)-1):
                            self.add_campaign_numbers('u_shape', clicks[i].partner.id, clicks[i].channel.id, clicks[i].campaign.id, (order.value * 0.2) / (len(clicks) - 2) )
                    
                    
                    for i in range(0, len(clicks)):
                        self.add_campaign_numbers('linear', clicks[i].partner.id, clicks[i].channel.id, clicks[i].campaign.id, order.value / len(clicks))
                    
                    
                    damping = 0.2
                    norm = sum(map(lambda i:math.exp(-damping*(len(clicks)-i-1)),range(0,len(clicks))))
                    
                    reduced_campaigns = {}
                    
                    for i in range(0, len(clicks)):
                        self.add_campaign_numbers('decay', clicks[i].partner.id, clicks[i].channel.id, clicks[i].campaign.id, order.value * math.exp(-damping * (len(clicks) - i - 1)) / norm)
                        campaign_cost_rows = Attributions.objects.all().filter(
                            date        = order.ordered_at.strftime('%Y-%m-%d'), 
                            channel_id  = clicks[i].channel.id, 
                            campaign_id = clicks[i].campaign.id,
                            partner_id  = clicks[i].partner.id
                        )
                        
                        if len(campaign_cost_rows):
                            for ccost in campaign_cost_rows:
                                cpp = (float(ccost.cost)/float(ccost.orders))
                                self.add_campaign_numbers('cost', clicks[i].partner.id, clicks[i].channel.id, clicks[i].campaign.id, cpp)
                            
                    last_click_channel = clicks[len(clicks)-1].channel.id
                    last_click_campaign = clicks[len(clicks)-1].campaign.id
                    last_click_partner = clicks[len(clicks)-1].partner.id
                    self.add_revenue_numbers('last_click', last_click_partner, last_click_channel, last_click_campaign, order.revenue)
                    
                    
                    first_click_channel = clicks[0].channel.id
                    first_click_campaign = clicks[0].campaign.id
                    first_click_partner = clicks[0].partner.id
                    self.add_revenue_numbers('first_click', 
                                              first_click_partner,
                                              first_click_channel, 
                                              first_click_campaign, 
                                              order.revenue
                                              )
    
                    if(len(clicks) == 2):
                        self.add_revenue_numbers('u_shape', clicks[0].partner.id, clicks[0].channel.id, clicks[0].campaign.id, order.revenue * 0.5)
                        self.add_revenue_numbers('u_shape', clicks[1].partner.id, clicks[1].channel.id, clicks[1].campaign.id, order.revenue * 0.5)
                    if(len(clicks) == 1):
                        self.add_revenue_numbers('u_shape', clicks[0].partner.id, clicks[0].channel.id, clicks[0].campaign.id, order.revenue)
                    if(len(clicks) > 2):
                        self.add_revenue_numbers('u_shape', clicks[0].partner.id, clicks[0].channel.id, clicks[0].campaign.id, order.revenue * 0.4)
                        self.add_revenue_numbers('u_shape', clicks[len(clicks)-1].partner.id, clicks[len(clicks)-1].channel.id, clicks[len(clicks)-1].campaign.id, order.revenue * 0.4)
                        for i in range(1, len(clicks)-1):
                            self.add_revenue_numbers('u_shape', clicks[i].partner.id, clicks[i].channel.id, clicks[i].campaign.id, (order.revenue * 0.2) / (len(clicks) - 2) )
                    
                    
                    for i in range(0, len(clicks)):
                        self.add_revenue_numbers('linear', clicks[i].partner.id, clicks[i].channel.id, clicks[i].campaign.id, order.revenue / len(clicks))
                    
                    
                    damping = 0.2
                    norm = sum(map(lambda i:math.exp(-damping*(len(clicks)-i-1)),range(0,len(clicks))))
                    
                    for i in range(0, len(clicks)):
                        self.add_revenue_numbers('decay', clicks[i].partner.id, clicks[i].channel.id, clicks[i].campaign.id, order.revenue * math.exp(-damping * (len(clicks) - i - 1)) / norm)

                for (partner, channel, campaign) in self.channel_attributions:
                        key = (partner, channel, campaign)
                        
                        cust_clv             = CustomerCLV()        
                        cust_clv.orders      = self.order_counter
                        cust_clv.order_id    = order.order_id
                        cust_clv.clv_total   = clv
                        cust_clv.clv_added   = order.value
                        days                 = (first_ordered_at - order.ordered_at).days * -1
                        cust_clv.days        = days
                        cust_clv.customer    = self.customer
                        cust_clv.first_ordered_at = first_ordered_at
                        cust_clv.date        = order.ordered_at
                        cust_clv.partner_id  = partner
                        cust_clv.channel_id  = channel
                        cust_clv.campaign_id = campaign
                        
                        cust_clv.clv_u_shape_total     = self.channel_attributions[key]['u_shape']
                        cust_clv.clv_linear_total      = self.channel_attributions[key]['linear']
                        cust_clv.clv_first_click_total = self.channel_attributions[key]['first_click']
                        cust_clv.clv_last_click_total  = self.channel_attributions[key]['last_click']
                        cust_clv.clv_decay_total       = self.channel_attributions[key]['decay']
                        
                        cust_clv.cost_total            = self.channel_attributions[key]['cost']
                        
                        cust_clv.revenue_u_shape_total     = self.revenue_attributions[key]['u_shape']
                        cust_clv.revenue_linear_total      = self.revenue_attributions[key]['linear']
                        cust_clv.revenue_first_click_total = self.revenue_attributions[key]['first_click']
                        cust_clv.revenue_last_click_total  = self.revenue_attributions[key]['last_click']
                        cust_clv.revenue_decay_total       = self.revenue_attributions[key]['decay']
                        
                        try: 
                            if orders[next_iindex]:
                                cust_clv.days_distance = (orders[next_iindex].ordered_at - order.ordered_at).days
                        except IndexError:
                                # the last day distance is 0
                                cust_clv.days_distance = 0
                        
                        if self.order_counter in self.channel_attr_per_order:
                            cust_clv.clv_u_shape_added     = self.channel_attr_per_order[self.order_counter][key]['u_shape']
                            cust_clv.clv_linear_added      = self.channel_attr_per_order[self.order_counter][key]['linear']
                            cust_clv.clv_first_click_added = self.channel_attr_per_order[self.order_counter][key]['first_click']
                            cust_clv.clv_last_click_added  = self.channel_attr_per_order[self.order_counter][key]['last_click']
                            cust_clv.clv_decay_added       = self.channel_attr_per_order[self.order_counter][key]['decay']
                            
                            cust_clv.cost_added            = self.channel_attr_per_order[self.order_counter][key]['cost']
                            
                            cust_clv.revenue_u_shape_added     = self.revenue_attr_per_order[self.order_counter][key]['u_shape']
                            cust_clv.revenue_linear_added      = self.revenue_attr_per_order[self.order_counter][key]['linear']
                            cust_clv.revenue_first_click_added = self.revenue_attr_per_order[self.order_counter][key]['first_click']
                            cust_clv.revenue_last_click_added  = self.revenue_attr_per_order[self.order_counter][key]['last_click']
                            cust_clv.revenue_decay_added       = self.revenue_attr_per_order[self.order_counter][key]['decay']
                            
                        
                        cust_clv_entries.append(cust_clv)
                        
            CustomerCLV.objects.bulk_create(cust_clv_entries)


                    
customers = Customer.objects.all()#.filter(customer_id=)
for customer in customers:
    customer_processor = CustomerProcessor(customer)
    customer_processor.start()
    db.reset_queries()