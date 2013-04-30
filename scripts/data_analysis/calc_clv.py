import sys, os
import argparse
import math

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../.."))

import logging



import cc_django.settings as settings
from django.core.management import setup_environ

setup_environ(settings)

from utils.models import *

def add(type, channel, campaign, value):
    channel = int(channel) 
    campaign = int(campaign)
    if not channel  in channel_attributions:
        channel_attributions[channel] = {}
    if not campaign in channel_attributions[channel]:
        channel_attributions[channel][campaign] = {
            'linear': 0.00, 
            'first_click': 0.00, 
            'last_click': 0.00, 
            'exponential_decay': 0.00,
            'u_shape': 0.00,
            'cost': 0.00
        }
    
    channel_attributions[channel][campaign][type] += value

channel_attributions = {}
customers = Customer.objects.all()
for customer in customers:
    orders = customer.orders().order_by('ordered_at')
    clv = 0
    marketing_cost = 0
    channel_attributions = {}
    if(len(orders)):
        order_counter = 1
        print "customer:%s" % (customer.id)
        first_ordered_at = None
        for order in orders:
            print "customer:%s ordercounter:%s/%s" % (customer.id, order_counter, len(orders))
            if not first_ordered_at:
                first_ordered_at = order.ordered_at
            
            order_products = OrderProducts.objects.filter(order_id=order.id)
            costs_product = sum(map(lambda op: op.cost_per_unit * op.qty, order_products))
            # costs_returns
            # order.value = order.revenue - (costs + cost_returns)
            order.value = order.revenue
            # order.save()
            clv               += order.value
            
            clicks = order.clicks()
            
            if(len(clicks)):
                last_click_channel = clicks[len(clicks)-1].channel.id
                last_click_campaign = clicks[len(clicks)-1].campaign.id
                add('last_click', last_click_channel, last_click_campaign, order.value)
                
                
                first_click_channel = clicks[0].channel.id
                first_click_campaign = clicks[0].campaign.id
                add('first_click', first_click_channel, first_click_campaign, order.value)

                if(len(clicks) == 2):
                    add('u_shape', clicks[0].channel.id, clicks[0].campaign.id, order.value * 0.5)
                    add('u_shape', clicks[1].channel.id, clicks[1].campaign.id, order.value * 0.5)
                if(len(clicks) == 1):
                    add('u_shape', clicks[0].channel.id, clicks[0].campaign.id, order.value)
                if(len(clicks) > 2):
                    add('u_shape', clicks[0].channel.id, clicks[0].campaign.id, order.value * 0.4)
                    add('u_shape', clicks[len(clicks)-1].channel.id, clicks[len(clicks)-1].campaign.id, order.value * 0.4)
                    for i in range(1, len(clicks)-1):
                        add('u_shape', clicks[i].channel.id, clicks[i].campaign.id, (order.value * 0.2) / (len(clicks) - 2) )
                
                
                for i in range(0, len(clicks)):
                    add('linear', clicks[i].channel.id, clicks[i].campaign.id, order.value / len(clicks))
                
                
                damping = 0.2
                norm = sum(map(lambda i:math.exp(-damping*(len(clicks)-i-1)),range(0,len(clicks))))
                
                reduced_campaigns = {}
                
                for i in range(0, len(clicks)):
                    add('exponential_decay', clicks[i].channel.id, clicks[i].campaign.id, order.value * math.exp(-damping * (len(clicks) - i - 1)) / norm)
                    campaign_cost_rows = Attributions.objects.all().filter(date=order.ordered_at.strftime('%Y-%m-%d'), 
                                                                         channel_id=clicks[i].channel.id, 
                                                                         campaign_id=clicks[i].campaign.id) 
                    if len(campaign_cost_rows):
                        for ccost in campaign_cost_rows:
                            cpp = (float(ccost.cost)/float(ccost.orders))
                            add('cost', clicks[i].channel.id, clicks[i].campaign.id, cpp)
                        
                    
            for channel in channel_attributions:
                for campaign in channel_attributions[channel]:
                    
                    cust_clv = CustomerCLV()        
                    cust_clv.orders      = order_counter
                    cust_clv.clv         = clv
                    days = (first_ordered_at - order.ordered_at).days * -1
                    cust_clv.days        = days
                    cust_clv.customer    = customer        
                    cust_clv.date        = order.ordered_at
                    cust_clv.channel_id  = channel
                    cust_clv.campaign_id = campaign
                    cust_clv.u_shape     = channel_attributions[channel][campaign]['u_shape']
                    cust_clv.linear      = channel_attributions[channel][campaign]['linear']
                    cust_clv.first_click = channel_attributions[channel][campaign]['first_click']
                    cust_clv.last_click  = channel_attributions[channel][campaign]['last_click']
                    cust_clv.decay       = channel_attributions[channel][campaign]['exponential_decay']
                    cust_clv.cost        = channel_attributions[channel][campaign]['cost']
                    cust_clv.save()     
                    #cust_clv          = CustomerCLV()
                    #cust_clv.customer = customer
                    #cust_clv.date     = order.ordered_at
                    #cust_clv.days     = (first_ordered_at - order.ordered_at).days
                    #cust_clv.orders   = order_counter
                    #cust_clv.clv      = clv
            
                    #cust_clv.save()
            
            
            order_counter += 1
