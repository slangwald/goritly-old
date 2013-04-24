import sys, os
import argparse
import datetime
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../.."))

import logging



import cc_django.settings as settings
from django.core.management import setup_environ

setup_environ(settings)

from utils.models import *
from django.db.models import *


orders = Order.objects.all().order_by('ordered_at')

for order in orders:
    clickchain = Click.objects.all().order_by('clicked_at').filter(
                                            customer_id=order.customer.id
                                    ).filter(
                                            clicked_at__lte = order.ordered_at
                                    ).filter(
                                             clicked_at__gte = order.ordered_at - datetime.timedelta(days=30)
                                    )
    if(len(clickchain)):
        position_in_chain = 1
        for click in clickchain:
            ch = Order2Clickchain()
            ch.order      = order
            ch.clicked_at = click.clicked_at
            ch.ordered_at = order.ordered_at
            ch.position   = position_in_chain
            ch.campaign   = click.campaign
            ch.partner    = click.partner
            ch.channel    = click.channel
            ch.keyword    = click.keyword
            ch.save()
            
            position_in_chain += 1