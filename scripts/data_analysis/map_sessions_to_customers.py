import sys
import datetime
import argparse

import cc_django.apps.utils.models as models
import cc_django.settings as settings

from django.core.management import setup_environ

setup_environ(settings)


if __name__ == '__main__':
#    customer_ids = models.CustomerIdMapping.collection.find()
    customer_ids = sorted(models.CustomerIdMapping.collection.distinct('custom var value 2'))
    for customer_id in customer_ids:
        customer = models.Customer.collection.find_one({'customer_id':customer_id})
        if not customer:
            customer = models.Customer(customer_id = customer_id)
        custom_var_values = map(lambda x:x['custom var value 1'],models.CustomerIdMapping.collection.find({'custom var value 2':customer_id}))
        customer['custom_var_1_values'] = custom_var_values
        customer['order_count'] = customer.orders().count()
        customer['click_count'] = customer.clicks().count()
        customer['order_value'] = sum(map(lambda order:order['Order value'],customer.orders()))
        media = {}
        for click in customer.clicks():
            if not click['medium'] in media.keys():
                media[click['medium']] = 1
            else:
                media[click['medium']]+=1
        customer['click_media'] = media
        print "%d clicks and %d orders with total value %g for customer %d" % (customer['click_count'],customer['order_count'],customer['order_value'],customer_id)
        customer.save()
