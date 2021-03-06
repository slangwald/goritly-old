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
    date        = models.DateField(db_index=True)
    channel     = models.ForeignKey(Channel)
    partner     = models.ForeignKey(Partner)
    campaign    = models.ForeignKey(Campaign)
    ad_group    = models.ForeignKey(AdGroup, null = True)
    ad_title    = models.ForeignKey(AdTitle, null = True)
    keyword     = models.ForeignKey(Keyword)
    match_type  = models.ForeignKey(MatchType)
    cost        = models.FloatField(default = 0.00)
    clicks      = models.IntegerField(default=0)

class Attributions(Commons):
    date        = models.DateField(db_index=True)
    channel     = models.ForeignKey(Channel)
    campaign    = models.ForeignKey(Campaign)
    partner     = models.ForeignKey(Partner)
    u_shape     = models.FloatField(default = 0.00)
    linear      = models.FloatField(default = 0.00)
    first_click = models.FloatField(default = 0.00)
    last_click  = models.FloatField(default = 0.00)
    decay       = models.FloatField(default = 0.00)
    cost        = models.FloatField(default = 0.00)
    orders      = models.IntegerField(default = 0)

class BrandKeywords(CommonDimensionModel):
    pass

class Visitor(Commons):
    identifier = models.CharField(max_length = 255)

class Customer(Commons):
    identifier = models.CharField(max_length = 255)
    def clickchain(self, date = None):
        clicks = Click.objects.all().filter(customer=self)
        return clicks
    
    def orders(self):
        orders = Order.objects.all().filter(customer=self)
        return orders
    
    def channels(self):
        """
        
        """
        return
        
    def campaigns(self):
        return
        
    def partners(self):
        return
    
    def keywords(self):
        return
    def clv(self, date):
        """
        the customers CLV (whole lifetime) at a specific date
        """
        return

class Order(Commons):
    visitor     = models.ForeignKey(Visitor, null = True)
    customer    = models.ForeignKey(Customer)
    order_id    = models.CharField(max_length = 255, db_index=True)
    ordered_at  = models.DateTimeField(db_index=True)
    value       = models.FloatField(default = 0.00, null = True)
    revenue     = models.FloatField(default = 0.00, null = True)
    tax         = models.FloatField(default = 0.00, null = True)
    shipping    = models.FloatField(default = 0.00, null = True)
    city        = models.CharField(max_length = 50, null = True)
    post_code   = models.CharField(max_length = 20, null = True)
    state       = models.CharField(max_length = 50, null = True)
    country     = models.CharField(max_length = 50, null = True)
    
    def products(self):
        return OrderProducts.objects.filter(order=self)
    def clicks(self):
        return Click.objects.filter(order=self)

class CustomerCLV(Commons):
    customer    = models.ForeignKey(Customer)
    date        = models.DateField()
    days        = models.IntegerField(default=0, db_index=True)
    
    days_distance = models.IntegerField(default=None, null=True, db_index=True)
    
    first_ordered_at = models.DateField(db_index=True)
    orders      = models.IntegerField(default=0)
    order_id    = models.CharField(max_length = 255, db_index=True)
    clv_total   = models.FloatField(default = 0.00)
    clv_added   = models.FloatField(default = 0.00)
    channel     = models.ForeignKey(Channel)
    campaign    = models.ForeignKey(Campaign)
    partner     = models.ForeignKey(Partner)
    
    clv_u_shape_total     = models.FloatField(default = 0.00)
    clv_linear_total      = models.FloatField(default = 0.00)
    clv_first_click_total = models.FloatField(default = 0.00)
    clv_last_click_total  = models.FloatField(default = 0.00)
    clv_decay_total       = models.FloatField(default = 0.00)
    
    clv_u_shape_added     = models.FloatField(default = 0.00) 
    clv_linear_added      = models.FloatField(default = 0.00) 
    clv_first_click_added = models.FloatField(default = 0.00) 
    clv_last_click_added  = models.FloatField(default = 0.00) 
    clv_decay_added       = models.FloatField(default = 0.00) 

    cost_added  = models.FloatField(default = 0.00)
    cost_total  = models.FloatField(default = 0.00)
    
    revenue_u_shape_total     = models.FloatField(default = 0.00)
    revenue_linear_total      = models.FloatField(default = 0.00)
    revenue_first_click_total = models.FloatField(default = 0.00)
    revenue_last_click_total  = models.FloatField(default = 0.00)
    revenue_decay_total       = models.FloatField(default = 0.00)
    
    revenue_u_shape_added     = models.FloatField(default = 0.00) 
    revenue_linear_added      = models.FloatField(default = 0.00) 
    revenue_first_click_added = models.FloatField(default = 0.00) 
    revenue_last_click_added  = models.FloatField(default = 0.00) 
    revenue_decay_added       = models.FloatField(default = 0.00) 
    
    


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
    
class OrderProductsReturns(Commons):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    qty = models.FloatField(default = 1)

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
    