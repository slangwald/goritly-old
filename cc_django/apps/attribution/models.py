# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

import datetime
import json

class CURRENCY:
    """
    Put currency codes here.
    """

    EURO = 0
    DOLLAR = 1

# Create your models here.
class Commons(models.Model):

    """
    Contains fields an functions common to all models below. Mainly convenience fields such as creation & modification date, as well as a generic data field that can be serialized using JSON.
    """

    created_at = models.DateTimeField(default = datetime.datetime.now,auto_now_add=True)
    modified_at = models.DateTimeField(default = datetime.datetime.now,auto_now=True)

    data = models.TextField(default = '')

    def set_data(self,data):
        self.data = json.dumps(data)
        
    def get_data(self):
        if self.data == '':
            return None
        return json.loads(self.data)

    class Meta:
        abstract = True

#campaign    source  medium  keyword custom var value 1  date    hour    new visits  visits  goal 1 completions

class GACampaign(Commons):

    """
    Represents a GA campaign.
    """

    name = models.CharField(max_length = 255,default = '')

class GASource(Commons):

    """
    Represents a GA source.
    """

    name = models.CharField(max_length = 255,default = '')

class GAMedium(Commons):

    """
    Represents a GA medium.
    """

    name = models.CharField(max_length = 255,default = '')

class GAKeyword(Commons):

    """
    Represents a GA keyword.
    """

    name = models.CharField(max_length = 255,default = '')

class GAClick(Commons):

    """
    Represents a GA click.
    """

    campaign = models.ForeignKey(GACampaign,null = True,blank = True)
    source = models.ForeignKey(GASource,null = True,blank = True)
    medium = models.ForeignKey(GAMedium,null = True,blank = True)
    keyword = models.ForeignKey(GAKeyword,null = True,blank = True)

    custom_var_1 = models.CharField(max_length = 255,default = '')
    custom_var_2 = models.CharField(max_length = 255,default = '')
    clicked_at = models.DateTimeField(blank = True,null = True)
    new_visits = models.IntegerField(default = 0)
    visits = models.IntegerField(default = 0)
    goal_1_completions = models.IntegerField(default = 0)
    goal_2_completions = models.IntegerField(default = 0)

class GACustomer(Commons):

    """
    Represents a GA customer.
    """

    identifier = models.CharField(max_length = 32)

class GASession(Commons):

    """
    Represents a GA session.
    """

    identifier = models.CharField(max_length = 32)

class GACustomerSession(Commons):

    """
    Matches GASession with GACustomer.
    """

    matched_at = models.DateTimeField()
    session = models.ForeignKey(GASession)
    customer = models.ForeignKey(GACustomer)
    visits = models.IntegerField(default = 0)

class MarketingCost(Commons):

    """
    Represents the marketing cost associated with a given source, campaign, medium and keyword for a given date.
    Can be used to model AdWords, FB, Affiliate or any other kind of marketing cost.
    """

    source = models.ForeignKey(GASource,blank = True,null = True)
    campaign = models.ForeignKey(GACampaign,blank = True,null = True)
    medium = models.ForeignKey(GAMedium,blank = True,null = True)
    keyword = models.ForeignKey(GAKeyword,blank = True,null = True)
    session = models.ForeignKey(GASession,blank = True,null = True)
    
    cost = models.FloatField(default = 0.00)
    currency = models.IntegerField(default = 0)

    date = models.DateTimeField()

class Order(Commons):

    """
    Represents an order.
    """

    order_id = models.CharField(max_length = 64)

    customer = models.ForeignKey(GACustomer)
    session = models.ForeignKey(GASession,blank = True,null = True)

    ordered_at = models.DateTimeField()

    order_value = models.FloatField(default = 0.00)
    promotion_code = models.CharField(max_length = 255,default = '')
    promotion_value = models.FloatField(default = 0.000)

    currency = models.IntegerField(default = 0)

