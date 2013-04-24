import sys, os
import argparse
import csv
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../.."))

import logging



import cc_django.settings as settings
from django.core.management import setup_environ

setup_environ(settings)

from utils.models import *

class CsvImporter():
    skip_first_row = True
    def __init__(self, filename):
        self.filename = filename
    
    def start_import(self):
        logging.critical('starting import for %s' % self.__class__.__name__)
        
        with open(self.filename, 'r') as csvfile:
            filereader = csv.reader(csvfile, delimiter=';')
            rowcount = 0
            for row in filereader:
                rowcount += 1
                if(rowcount == 1 and self.skip_first_row == True):
                    continue
                row = self.cleanup_row(row)
                self.save_row(row)

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
    
    def save_row(self, row):
        channel   , created  = Channel  .objects.get_or_create(name=row[1])
        partner   , created  = Partner  .objects.get_or_create(name=row[2])
        campaign  , created  = Campaign .objects.get_or_create(name=row[3])
        ad_group  , created  = AdGroup  .objects.get_or_create(name=row[4])
        ad_title  , created  = AdTitle  .objects.get_or_create(name=row[5])
        keyword   , created  = Keyword  .objects.get_or_create(name=row[6])
        match_type, created  = MatchType.objects.get_or_create(name=row[7])
        
        mc = MarketingCost()
        
        mc.date        = row[0]
        mc.cost        = row[8]
        
        mc.channel     = channel   
        mc.partner     = partner   
        mc.campaign    = campaign  
        mc.ad_group    = ad_group  
        mc.ad_title    = ad_title  
        mc.keyword     = keyword   
        mc.match_type  = match_type
        mc.save()
        
class CsvClickChain(CsvImporter):
    def save_row(self, row):
        # 0         1            2    3    4        5        6        7                8                    9            10
        ['1212312', '2013-01-01', '1', '', 'cpc', 'google', 'shoes', 'green shoes', 'green shoes 70% off', 'budget gps', 'broad']
        
        
        campaign , created = Campaign.objects.get_or_create(name=row[6])
        partner  , created = Partner.objects.get_or_create(name=row[5])
        channel  , created = Channel.objects.get_or_create(name=row[4])
        keyword  , created = Keyword.objects.get_or_create(name=row[9])
                            
        visitor , created  = Visitor.objects.get_or_create(identifier=row[0])
        #customer     = Customer
        
        cl = Click()
        
        cl.campaign = campaign
        cl.partner  = partner 
        cl.channel  = channel 
        cl.keyword  = keyword 
        cl.visitor  = visitor 
        cl.clicked_at   = row[1]
        #new_visits   = models.
        cl.visits       = row[2]
        if (row[3].isdigit()):
            cl.goal_1_completions = row[3]
        #goal_2_completions =
        cl.save()
        

class CsvOrders(CsvImporter):
    #skip_first_row = False
    def save_row(self, row):
        # 0                    1                2        3                    4            5        6             7    8            9        10
        ['unique visitor id', 'customer id', 'order id', 'order timestamp', 'order value', 'tax', 'shipping', 'city', 'post code', 'state', 'country']
        
        visitor,  created = Visitor.objects.get_or_create(identifier=row[0])
        customer, created = Customer.objects.get_or_create(identifier=row[1])
        
        o = Order()
        
        o.visitor     = visitor
        o.customer    = customer
        o.order_id    = row[2]
        o.ordered_at  = row[3]
        o.revenue     = row[4]
        o.tax         = row[5]
        o.shipping    = row[6]
        o.city        = row[7]
        o.post_code   = row[8]
        o.state       = row[9]
        o.country     = row[10]
        o.save()

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
    
        
        
    
    