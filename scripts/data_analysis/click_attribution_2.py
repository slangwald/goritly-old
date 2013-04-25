import sys, os
import datetime
import argparse
import math
import itertools
import pprint

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../.."))


import cc_django.settings as settings
from django.core.management import setup_environ
setup_environ(settings)

import cc_django.apps.utils.models as models

import datetime

from django.core.management import setup_environ



"""
This script implements various forms of click attribution, e.g.
-last click
-first click
-exponential decay
- u shape (40-20-40)
"""


if __name__ == '__main__':
    paying_customers = models.Customer.objects.all()
    attributions = {
        'last_click': {},
        'first_click': {},
        'exponential_decay': {},
        'u_shape': {}
    }
    revenue_tree = {}
    click_combinations = []
    click_combinations_revenue = {}
    channels = []

    def add(type,channel,value):
        if not channel in attributions[type]:
            attributions[type][channel] = 0
        attributions[type][channel]+=value
        
    def add_click_combination(path,revenue):
        
        reduced_path = {}
        for element in sorted(path):
            if not element in channels:
                channels.append(element)
            if not element in reduced_path:
                reduced_path[element] = 0
            reduced_path[element]+=1
        if not reduced_path in click_combinations:
            click_combinations.append(reduced_path)
        i = click_combinations.index(reduced_path)
        if not i in click_combinations_revenue:
            click_combinations_revenue[i] = (0,0)
        current_values = click_combinations_revenue[i]
        click_combinations_revenue[i]  =(current_values[0]+1,current_values[1]+revenue)
        
    def get_value_added_by_channels(channels):
        total_revenue = 0
        revenue = 0
        for i in click_combinations_revenue:
            click_path = click_combinations[i].copy()
            altered = False
            for channel in channels:
                if channel in click_path.keys():
                    del click_path[channel]
                    altered = True
            if altered:
                if click_path and click_path in click_combinations:
                    j = click_combinations.index(click_path)
                    revenue_per_event = click_combinations_revenue[j][1]/float(click_combinations_revenue[j][0])
                    revenue+=revenue_per_event*click_combinations_revenue[i][0]
            else:
                revenue+=click_combinations_revenue[i][1]
            total_revenue+=click_combinations_revenue[i][1]
        return total_revenue-revenue
        
    def add_to_tree(path,revenue):
        path_values = []
        for value in path:
            if not value in path_values:
                path_values.append(value)
        for j in range(0,min(3,len(path_values))):
            permutations = itertools.permutations(path_values, j + 1)
            for permutation in permutations:
                current_root = revenue_tree
                for element in permutation:
                    if not element in current_root:
                        current_root[element] = {'value':0,'children':{}}
                    current_root[element]['value'] += revenue
                    current_root = current_root[element]['children']
        
    unattributed_revenue = 0
    total_value = 0
    for customer in paying_customers:
        print "\n\nCustomer %d" % customer.id
        orders = customer.orders()
        print orders
        if(len(orders) < 1):
            continue
        
        for order in orders:
            total_value += order.value
            
            clicks = customer.clickchain().filter(order_id=order.id)
            
            #clicks = list(customer.clicks({'date':{'$lte':order['Order date'] + datetime.timedelta(days = 1)}}).sort('date'))
            print "%d relevant clicks for order value %g, %d total clicks" % (len(clicks), order.value, clicks.count())
            add_to_tree(map(lambda x:x.channel.name ,clicks),order.value)
            if len(clicks):
                add_click_combination(map(lambda x:x.channel.name, clicks), order.value)
                last_click_channel = clicks[len(clicks)-1].channel.name
                add('last_click', last_click_channel, order.value)
                first_click_channel = clicks[0].channel.name
                add('first_click', first_click_channel, order.value)

                if(len(clicks) == 2):
                    add('u_shape', clicks[0].channel.name, order.value * 0.5)
                    add('u_shape', clicks[1].channel.name, order.value * 0.5)
                if(len(clicks) == 1):
                    add('u_shape', clicks[0].channel.name, order.value)
                if(len(clicks) > 2):
                    add('u_shape', clicks[0].channel.name, order.value * 0.4)
                    add('u_shape', clicks[len(clicks)-1].channel.name, order.value * 0.4)
                    for i in range(1, len(clicks)-1):
                        add('u_shape', clicks[i].channel.name, (order.value * 0.2) / (len(clicks) - 2) )
                
                
                damping = 0.2
                norm = sum(map(lambda i:math.exp(-damping*(len(clicks)-i-1)),range(0,len(clicks))))
                for i in range(0, len(clicks)):
                    add('exponential_decay', clicks[i].channel.name, order.value * math.exp(-damping * (len(clicks) - i - 1)) / norm)
                    
            else:
                unattributed_revenue += order.value
    print "Total value: %g" % total_value
    print "Unattributed revenue: %g" % unattributed_revenue
    print "Last click attribution: %g" % sum(attributions['last_click'].values())
    print attributions['last_click']
    print "First click attribution: %g" % sum(attributions['first_click'].values())
    print attributions['first_click']
    print "Exponential decay: %g" % sum(attributions['exponential_decay'].values())
    print attributions['exponential_decay']
    print "u_shape: %g" % sum(attributions['u_shape'].values())
    print attributions['u_shape']
    
    total_added_value = 0
    for channel in channels:
        added_value = get_value_added_by_channels([channel])
        print "Channel %s added value: %g" % (channel, added_value)
        total_added_value += added_value
    print "Total added value: %g" % total_added_value
    for permutation in itertools.combinations(channels, 2):
        added_value = get_value_added_by_channels(permutation)
        print "Channels %s added value: %g" % (" & ".join(permutation),added_value)
