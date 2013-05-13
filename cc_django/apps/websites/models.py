# -*- coding: utf-8 -*-
import datetime
import os.path
import json
import hashlib
import re

from django.db import models
from django.db import IntegrityError
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse,resolve

from profiles.models import Commons,Image

class Website(Commons):
    
    logo = models.ForeignKey(Image,blank = True,default = None,null = True,related_name = 'website_logos',on_delete = models.SET_NULL) 
        
    name = models.CharField(max_length = 200,default = '')
    description = models.TextField(default = '')
          
    is_active = models.BooleanField(default = True)
    
    admins = models.ManyToManyField(User,related_name = 'website_admins')
    owners = models.ManyToManyField(User,related_name = 'website_owners')
    
    db_name = models.CharField(max_length = 20)
    