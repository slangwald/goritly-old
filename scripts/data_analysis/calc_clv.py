import sys, os
import argparse
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../.."))

import logging



import cc_django.settings as settings
from django.core.management import setup_environ

setup_environ(settings)

from utils.models import *

customers = Customer.objects.all()
for customer in customers:
    orders = customer.orders().order_by('ordered_at')
    clv = 0
    print len(orders)
    if(len(orders)):
        order_counter = 1
        for order in orders:

            order_products = OrderProducts.objects.filter(order_id=order.id)
            costs = sum(map(lambda op: op.cost_per_unit * op.qty, order_products))
            order.value = order.revenue - costs
            order.save()
            clv += order.value
            
            cust_clv          = CustomerCLV()
            cust_clv.customer = customer
            cust_clv.date     = order.ordered_at
            cust_clv.orders   = order_counter
            cust_clv.clv      = clv
            
            #cust_clv.save()
            
            order_counter += 1
