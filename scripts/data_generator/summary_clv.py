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

from cc_django.apps.attribution.models import *

"""
Data generator

200 customer
Website ID always 1
1-9 orders

from Jun 2009 - Mar 2013
"""


from random import *
import time

class Generator:
	def generate(self):
		
		time_start = int((time.time() - (86400 * 365 * 4)))
		time_end = int(time.time())
		
		global_order_counter = 0
		for customer_counter in range(1, 20):
			first_click_ts = randint(time_start, time_end)
			first_click = datetime.datetime.fromtimestamp(first_click_ts)
			
			last_click_ts = first_click_ts
			last_click = first_click
			
			first_order_date = first_click
			
			for order_counter in range(randint(1, 9)):
				global_order_counter += 1
				
				order_date = last_click
				
				website = Website()
				website.id = 1

				summary = SummaryCLV()
				
				summary.website = website 
				summary.customer_id = customer_counter
				summary.order_id = global_order_counter
				summary.date_click = first_click
				summary.channel  = None
				summary.partner = None
				summary.campaign = None
				summary.adgroup = None
				summary.adtitle = None
				summary.keyword = None
				summary.match_type = None
				summary.date_order = last_click
				summary.date_customer = first_order_date
				summary.date_clv = last_click 
				summary.counter  = order_counter
				summary.customer_age = int((last_click_ts - first_click_ts)/86400)
				summary.contribution_to_clv = 0.3
				summary.marketing_cost = 2.00
				summary.revenue_order = 30
				summary.profit_order = 20
				summary.profit_order_after_returns = 17
				summary.revenue = 20
				summary.revenue_click = 0.3
				summary.profit = 3
				summary.profit_click = 3
				summary.clv = 40
				summary.clv_click = 10
				summary.marketing_cost_click = 20
				summary.roi = 120.5
				
				summary.save()
				
				last_click_ts = randint(last_click_ts, time_end)
				last_click = datetime.datetime.fromtimestamp(last_click_ts)
		
		return

		
if __name__ == '__main__':
	gen = Generator()
	gen.generate()

		