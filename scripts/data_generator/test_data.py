import os
import sys
import datetime
import argparse
import math
import itertools
import pprint

import datetime

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../.."))

import cc_django.settings as settings
from django.core.management import setup_environ
setup_environ(settings)

from cc_django.apps.utils.models import *

"""
Data generator

200 customer
Website ID always 1
1-9 orders

from Jun 2009 - Mar 2013
"""


from random import *
import time

class CustomerGenerator:
    
    customer = None
    visitor = None
    customer_orders = []
    
    
    partner = ['google', 'facebook', 'groupon']
    channel = {
               'google'   : ['sem generic'      , 'sem other'   ],
               'facebook' : ['social media paid', 'social other'],
               'groupon'  : ['coupons'          , 'grp1'        ]
              }
    campaigns = {
                 
                 'sem generic'      : ['special shoes', 'nike stuff', 'addidas happyshoe'], 
                 'sem other'        : ['demand-mining', 'hellokitty', 'special users'],
                 'social media paid': ['valentines day special',  'male 25-29', 'females 18-24'],
                 'social other'     : ['win an ipad 2013', 'social other 1', 'social other 2'],
                 'coupons'          : ['95% off for all products', 'coupon 1', 'coupon 2'],
                 'grp1'             : ['grp1.1', 'grp1.2', 'grp1.3']
                 }
    
    products = ['Shoe1', 'Shoe2', 'Shoe3']
    prices = {
              'Shoe1': 45.99, 
              'Shoe2': 23.95, 
              'Shoe3': 99.98
              }
    
    def generate(self):
        
        for customer_counter in range(1, 2000):
            print customer_counter
            self.generate_customer(customer_counter)
            self.generate_orders()
            self.generate_clickchain()
            
        return
    
    def generate_clickchain(self):
        for order in self.customer_orders:
            for clicks in range(randint(1, 9)):
                click = Click()
                
                partner_index    = self.partner[randint(0, 2)]
                channel_index    = self.channel[partner_index][randint(0,1)]
                campaign_index   = self.campaigns[channel_index][randint(0,2)]
                
                
                channel   , created  = Channel  .objects.get_or_create(name=channel_index)
                partner   , created  = Partner  .objects.get_or_create(name=partner_index)
                campaign  , created  = Campaign .objects.get_or_create(name=campaign_index)
                
                click.channel   = channel 
                click.partner   = partner 
                click.campaign  = campaign
                
                click.visitor    = self.visitor
                click.customer   = self.customer
                click.order      = order
                click.save()
    
    def generate_customer(self, customer_id):
        c = Customer()
        c.identifier = customer_id
        c.save()
        
        v = Visitor()
        v.identifier = customer_id
        v.save()
        
        self.customer = c
        self.visitor = v
        
        day = randint(1, 31)
        self.customer_joined = datetime.datetime(2013, 1, day)
        
    
    def generate_orders(self):
        self.customer_orders = []
        for i in range(randint(1, 12)):    
            o = Order()
            o.visitor     = self.visitor
            o.customer    = self.customer
            o.order_id    = randint(10000000, 20000000)
            o.ordered_at  = datetime.datetime(2013, 1, randint(self.customer_joined.day, 31))
            o.value       = float(randint(2000, 6000)) / 100
            o.revenue     = o.value
            o.tax         = 0
            o.shipping    = 0
            o.save()
            self.customer_orders.append(o)
        
        return

class MarketingCostGenerator():
    partner = ['google', 'facebook', 'groupon']
    channel = {
               'google'   : ['sem generic'      , 'sem other'   ],
               'facebook' : ['social media paid', 'social other'],
               'groupon'  : ['coupons'          , 'grp1'        ]
              }
    campaigns = {
                 
                 'sem generic'      : ['special shoes', 'nike stuff', 'addidas happyshoe'], 
                 'sem other'        : ['demand-mining', 'hellokitty', 'special users'],
                 'social media paid': ['valentines day special',  'male 25-29', 'females 18-24'],
                 'social other'     : ['win an ipad 2013', 'social other 1', 'social other 2'],
                 'coupons'          : ['95% off for all products', 'coupon 1', 'coupon 2'],
                 'grp1'             : ['grp1.1', 'grp1.2', 'grp1.3']
                 }
    
    
    def generate(self):
        for partner in self.partner:
            for channel in self.channel[partner]:
                for campaign in self.campaigns[channel]:
                    for day in range(1,31):
                        mc = MarketingCost()
                        mc.date        = datetime.datetime(2013, 1, day)

                        ch , created  = Channel  .objects.get_or_create(name=channel)
                        pa , created  = Partner  .objects.get_or_create(name=partner)
                        ca , created  = Campaign .objects.get_or_create(name=campaign)
                        k  , created  = Keyword  .objects.get_or_create(name="bla")
                        mc.channel     = ch
                        mc.partner     = pa
                        mc.campaign    = ca
                        mc.keyword     = k
                        mc.match_type_id = 1
                        mc.cost        = randint(150, 500)
                        
                        mc.save()

        
            
        
        
if __name__ == '__main__':
    #gen = CustomerGenerator()
    gen = MarketingCostGenerator()
    gen.generate()

        