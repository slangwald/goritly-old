import sys, os
import argparse
import csv
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../.."))

import logging



import cc_django.settings as settings
from django.core.management import setup_environ
from datetime import datetime, time

setup_environ(settings)

from utils.models import *
import math

from django import db


class CsvImporter():
    skip_first_row = True
    def __init__(self, filename):
        self.filename = filename
    
    def start_import(self):
        logging.critical('starting import for %s' % self.__class__.__name__)
        errors = 0
        with open(self.filename, 'r') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',')
            rowcount = 0
            for row in filereader:
                rowcount += 1
                if(rowcount == 1 and self.skip_first_row == True):
                    continue
                row = self.cleanup_row(row)
                print "saving row %d" % (rowcount)
                self.save_row(row)
                db.reset_queries()
                
                #rate = errors*100/rowcount
                #print rate
                #print "%d errors on %d rows (ratio: %f %%)" % (errors, rowcount, rate)   

    def validate_row(self, row):
        pass
    
    def cleanup_row(self, row):
        lowercased = []
        for cell in row:
            lowercased.append(cell.strip().lower())
        return lowercased

    def save_row(self, row):
        
        pass

class CsvMarketingCost(CsvImporter):
    skip_first_row = True
    def save_row(self, row):
        ['date',          # 0
         'partner',       # 1
         'channel',       # 2
         'account',       # 3
         'campaign',      # 4
         'cost',          # 5
         'clicks',        # 6
         'impressions',   # 7
         'country',       # 8
         'keyword',       # 9
         'match type',    # 10
         'avg. position'] # 11
        
        #print row
        #sys.exit()

        #if row[8] != "sg":
        #    print "skipped (sg-filter) %s" % (row)
        #    return 0

        if row[5] == "0":
            print "skipped (cost-zero-filter) %s" % (row)
            return 1

        channel   , created  = Channel  .objects.get_or_create(name=row[2])
        partner   , created  = Partner  .objects.get_or_create(name=row[1])
        campaign  , created  = Campaign .objects.get_or_create(name=row[4])
        keyword   , created  = Keyword  .objects.get_or_create(name=row[9])
        match_type, created  = MatchType.objects.get_or_create(name=row[10])
        
        mc = MarketingCost()
        
        mc.date        = datetime.datetime.strptime(row[0], '%m/%d/%Y')
        mc.cost        = row[5]
        mc.click       = row[6]
        mc.channel     = channel   
        mc.partner     = partner   
        mc.campaign    = campaign  
        mc.ad_group    = None
        mc.ad_title    = None  
        mc.keyword     = keyword   
        mc.match_type  = match_type
        mc.save()
        
        return 0
        
class CsvClickChain(CsvImporter):
    skip_first_row = True
    def save_row(self, row):
        
        ['country',                                # 0
         'order id',                               # 1
         'partner',                                # 2
         'channel',                                # 3
         'account',                                # 4
         'campaign',                               # 5
         'position since customer journey start',  # 6
         'time in campaign lifecycle (days)'       # 7
         ]
        
        #print row
        
        #sys.exit()
        
        #if row[0] != "sg":
            #print "skipped (sg-filter) %s" % (row)
        #    return 0
        
        order = Order.objects.all().filter(order_id=row[1])
        
        if(len(order) == 0):
            print "skipped (not-exists-order-filter) %s" % (row)
            return 1
        
        if(len(order) > 0):
            campaign , created = Campaign.objects.get_or_create(name=row[5])
            partner  , created = Partner.objects.get_or_create(name=row[2])
            channel  , created = Channel.objects.get_or_create(name=row[3])
            keyword  , created = Keyword.objects.get_or_create(name='')
                                
            #visitor , created  = Visitor.objects.get_or_create(identifier=row[0])
            #customer     = Customer
            
            cl = Click()
            cl.order = order[0]
            cl.campaign = campaign
            cl.partner  = partner 
            cl.channel  = channel 
            cl.keyword  = keyword 
            #cl.visitor  = visitor 
            #cl.clicked_at   = row[1]
            #new_visits   = models.
            #cl.visits       = row[2]
            #if (row[3].isdigit()):
            #    cl.goal_1_completions = row[3]
            #goal_2_completions =
            cl.save()
        
        return 0
        

class CsvOrders(CsvImporter):
    skip_first_row = True
    def save_row(self, row):
        
        ['country',            # 0    SG,
         'order_id',           # 1            200937936,
         'order_date',         # 2            3/31/2013,
         'customer_id',        # 3            106277,
         'order_item_id',      # 4            296152,
         'sku',                # 5            BU871SH96TRN-266332,
         'sku_config',         # 6            BU871SH96TRN,
         'unit_price',         # 7            10,
         'paid_price',         # 8            10,
         'coupon_amount',      # 9            0,
         'tax_amount',         # 10           0.65,
         'original_unit_price',# 11           22.9,
         'cost',               # 12           6.07,
         'category',           # 13           Female Footwear,
         'cart_rule_discount', # 14           0,
         'cart_rule_name',     # 15           ,
         'voucher code']       # 16           ,
                               #               canceled
        
        country = row[0]
        
        visitor,  created = Visitor.objects.get_or_create(identifier= 'cust_' + row[3])
        customer, created = Customer.objects.get_or_create(identifier=row[3])
        
        print "%s - %s" % (row[3], customer.id)
        
        order_date = datetime.datetime.strptime(row[2], '%m/%d/%Y')
        o, created_order = Order.objects.get_or_create(customer_id=customer.id, 
                                                       order_id=row[1],
                                                       ordered_at=order_date)
        
        if created_order:
            o.visitor_id  = visitor.id
            o.customer_id = customer.id
            o.order_id    = row[1]
            o.ordered_at  = order_date
            o.revenue     = 0
            o.tax         = 0
            o.shipping    = 0
        
        o.revenue     += float(row[8])
        o.tax         += float(row[10])
        
        
        o.city        = None
        o.post_code   = None
        o.state       = None
        o.country     = country
        
        o.save()
        
        product_cat, created_cat = ProductCategory.objects.get_or_create(name=row[13])
        product, created_product = Product.objects.get_or_create(sku=row[5])
        
        if created_product:
            product.name = row[4]
            product.category = product_cat
            product.save()
        
        op, created_op = OrderProducts.objects.get_or_create(order_id=o.id, 
                                                             product_id=product.id,
                                                             price_per_unit = row[7],
                                                             cost_per_unit = row[12])
        
        # OrderProducts
        if created_op:
            op.order = o
            op.product = product
            op.price_per_unit = row[7]
            op.cost_per_unit = row[12]
            op.qty = 0
        
        op.qty += 1
        op.save()

class CsvOrderProducts(CsvImporter):
    def save_row(self, row):
        #    0                   1               2               3        4                5                    6            7            8
        ['unique visitor id', 'customer id', 'order id*', 'product sku', 'product name', 'product category', 'unit price', 'unit cost', 'quantity']
        
        
        #class ProductCategory(CommonDimensionModel):
        product_cat, created = ProductCategory.objects.get_or_create(name=row[5])
    
        #class Product(Commons):
        product, created = Product.objects.get_or_create(sku=row[3])
        
        if created:
            product.name = row[4]
            product.category = product_cat
            product.save()
        
    
        op = OrderProducts()
        # OrderProducts
        op.order = Order.objects.get(order_id=row[2])
        op.product = product
        op.qty = row[8]
        op.price_per_unit = row[6]
        op.cost_per_unit = row[7]
        
        op.save()
        

class CsvBrandKeywords(CsvImporter):
    
    def save_row(self, row):
        bk, created = BrandKeywords.objects.get_or_create(name=row[0])
        if(created == True):
            bk.save()
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Import CSV Files")
    parser.add_argument('--keywords-brand',type=str)
    parser.add_argument('--id-matching', type=str)
    parser.add_argument('--orders', type=str)
    parser.add_argument('--returns', type=str)
    parser.add_argument('--clickchain',  type=str)
    parser.add_argument('--marketing-cost',type=str)
    parser.add_argument('--products', type=str)
    parser.add_argument('--voucher', type=str)
    parser.add_argument('--utils-db', type=str)
    
    args = parser.parse_args()
    imports = []
    if(args.marketing_cost):
        imports.append(CsvMarketingCost(filename = args.marketing_cost))
    if(args.keywords_brand):
        imports.append(CsvBrandKeywords(filename = args.keywords_brand))
    if(args.clickchain):
        imports.append(CsvClickChain(filename = args.clickchain))
    if(args.orders):
        imports.append(CsvOrders(filename = args.orders))
    if(args.products):
        imports.append(CsvOrderProducts(filename = args.products))
        
    
    for importer in imports:
        importer.start_import()
    
        
        
    
    