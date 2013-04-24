import sys, os
import argparse
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../.."))

import logging



import cc_django.settings as settings
from django.core.management import setup_environ

setup_environ(settings)

from utils.models import *
from django.db.models import *

marketing_costs = MarketingCost.objects.raw('SELECT *, SUM(cost) as summed_cost FROM utils_marketingcost GROUP BY `date`, channel_id, campaign_id ORDER BY `date`')

for mc in marketing_costs:
    campaign_cost = ChannelAndCampaignCost()
    
    campaign_cost.date = mc.date
    campaign_cost.campaign = mc.campaign
    campaign_cost.channel = mc.channel
    campaign_cost.cost = mc.summed_cost
    
    order_turnover = 0
    
    clickchain = Order2Clickchain.objects.all() \
                    .filter(ordered_at=mc.date) \
                    .filter(campaign=mc.campaign) \
                    .filter(channel=mc.channel)
    
    if (len(clickchain) == 0):
        # Find out whats the next date where this channel matches
        clickchain = Order2Clickchain.objects.all() \
                    .filter(ordered_at__gt=mc.date) \
                    .filter(campaign=mc.campaign) \
                    .filter(channel=mc.channel)
    orders = map(lambda x: x.order, clickchain)
    
    campaign_cost.value = sum(map(lambda x: x.value, orders))
    
    campaign_cost.save()
    
    #campaign_cost.save()
