from django.db import models
from django.contrib.auth.models import User
import datetime
import json


class Commons(models.Model):

    """
    Contains fields an functions common to all models below. Mainly convenience fields such as creation & modification date, as well as a generic data field that can be serialized using JSON.
    """
    created_at = models.DateTimeField(default = datetime.datetime.now,auto_now_add=True)
    modified_at = models.DateTimeField(default = datetime.datetime.now,auto_now=True)
 
    class Meta:
        abstract = True

class CommonDimensionModel(Commons):
    name = models.CharField(max_length = 255)
    
    class Meta:
        abstract = True

    
class Channel(CommonDimensionModel):
    pass

class Partner(CommonDimensionModel):
    pass

class Campaign(CommonDimensionModel):
    pass

class AdGroup(CommonDimensionModel):
    pass

class AdTitle(CommonDimensionModel):
    pass

class Keyword(CommonDimensionModel):
    pass

class MatchType(CommonDimensionModel):
    pass

class MarketingCost(Commons):
    date        = models.DateTimeField()
    channel     = models.ForeignKey(Channel)
    partner     = models.ForeignKey(Partner)
    campaign    = models.ForeignKey(Campaign)
    ad_group    = models.ForeignKey(AdGroup, null = True)
    ad_title    = models.ForeignKey(AdTitle, null = True)
    keyword     = models.ForeignKey(Keyword)
    match_type  = models.ForeignKey(MatchType)
    cost        = models.FloatField(default = 0.00)
    clicks      = models.IntegerField(default=0)

class BrandKeywords(CommonDimensionModel):
    pass

class Visitor(Commons):
    identifier = models.CharField(max_length = 255)

class Customer(Commons):
    identifier = models.CharField(max_length = 255)
    pass

class Order(Commons):
    visitor     = models.ForeignKey(Visitor, null = True)
    customer    = models.ForeignKey(Customer)
    order_id    = models.CharField(max_length = 255)
    ordered_at  = models.DateTimeField()
    value       = models.FloatField(default = 0.00, null = True)
    revenue     = models.FloatField(default = 0.00, null = True)
    tax         = models.FloatField(default = 0.00, null = True)
    shipping    = models.FloatField(default = 0.00, null = True)
    city        = models.CharField(max_length = 50, null = True)
    post_code   = models.CharField(max_length = 20, null = True)
    state       = models.CharField(max_length = 50, null = True)
    country     = models.CharField(max_length = 50, null = True)
    

class CustomerCLV(Commons):
    customer = models.ForeignKey(Customer)
    date     = models.DateField()
    orders   = models.IntegerField(default=0)
    clv      = models.FloatField(default = 0.00)
    


class ProductCategory(CommonDimensionModel):
    pass

class Product(Commons):
    sku = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    category = models.ForeignKey(ProductCategory, null = True)
    

class OrderProducts(Commons):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    qty = models.FloatField(default = 1)
    price_per_unit = models.FloatField()
    cost_per_unit = models.FloatField()
    



class CustomerIdMap(Commons):
    visitor = models.ForeignKey(Visitor)
    customer = models.ForeignKey(Customer)

class Click(Commons):

    """
    Represents a click.
    """

    campaign = models.ForeignKey(Campaign,null = True,blank = True)
    partner = models.ForeignKey(Partner,null = True,blank = True)
    channel = models.ForeignKey(Channel,null = True,blank = True)
    keyword = models.ForeignKey(Keyword,null = True,blank = True)

    visitor = models.ForeignKey(Visitor, null = True)
    customer = models.ForeignKey(Customer, null = True)
    
    clicked_at = models.DateTimeField(blank = True,null = True)
    new_visits = models.IntegerField(default = 0)
    visits = models.IntegerField(default = 0)
    goal_1_completions = models.IntegerField(default = 0)
    goal_2_completions = models.IntegerField(default = 0)
    order = models.ForeignKey(Order, null = True)
    position_in_chain = models.IntegerField(null=True)
    
class ChannelAndCampaignCost(Commons):
    date = models.DateField()
    campaign = models.ForeignKey(Campaign,null = True,blank = True)
    channel = models.ForeignKey(Channel,null = True,blank = True)
    cost = models.FloatField(default = 0.00)
    
class Order2Clickchain(Commons):
    order = models.ForeignKey(Order)
    clicked_at = models.DateTimeField(blank = True,null = True)
    ordered_at = models.DateTimeField()
    position = models.IntegerField()
    campaign = models.ForeignKey(Campaign, null = True,blank = True)
    partner = models.ForeignKey(Partner, null = True,blank = True)
    channel = models.ForeignKey(Channel, null = True,blank = True)
    keyword = models.ForeignKey(Keyword, null = True,blank = True)
    
"""
class Click(orm.Document):
	pass

class Customer(orm.Document):
    
    class CustomerException(Exception):
        pass

    def clicks(self,filters = {}):
        if not 'custom_var_1_values' in self.keys():
            raise CustomerException("custom_var_1_value not defined!")
        filters['custom var value 1']= {'$in':self['custom_var_1_values']}
        return Click.collection.find(filters)

    def orders(self,filters = {}):
        filters['Customer ID'] = self['customer_id']
        return Order.collection.find(filters)

class CustomerIdMapping(orm.Document):
	pass

class Order(orm.Document):
	pass
    
"""