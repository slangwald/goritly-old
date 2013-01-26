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

import profiles.settings as settings
import global_settings
from profiles.utils.random_keys import generate_random_key,generate_unique_key

# Create your models here.
class Commons(models.Model):

	created_at = models.DateTimeField(default = datetime.datetime.now,auto_now_add=True)
	modified_at = models.DateTimeField(default = datetime.datetime.now,auto_now=True)
	unique_key = models.CharField(max_length = 32,default = '',null = True,blank = True)

	data = models.TextField(default = '')

	def set_data(self,data):
		self.data = json.dumps(data)
		
	def get_data(self):
		if self.data == '':
			return None
		return json.loads(self.data)
	
	def save(self,*args,**kwargs):
		if self.unique_key == '':
			self.unique_key = generate_unique_key()
		super(Commons,self).save(*args,**kwargs)
	
	class Meta:
		abstract = True
        
class ConfirmationKey(Commons):
	
	class KeyError(Exception):
		pass
	
	class TooManyKeysAlready(KeyError):
		pass
	
	class TooManyKeysSentRecently(KeyError):
		pass

	email = models.EmailField(blank = True,null = True)
	
	function = models.CharField(default = 'undefined',max_length = 200)
	key = models.CharField(max_length = 100,default = '',unique = True)

	created_by = models.ForeignKey(User,blank = True,null = True,on_delete = models.SET_NULL)
	
	is_valid = models.BooleanField(default = True)
	has_been_opened = models.BooleanField(default = False)

	has_been_sent = models.BooleanField(default = False)	
	failed_to_send = models.BooleanField(default = False)
	sent_at = models.DateTimeField(default = None,blank = True,null = True)

	object_id = models.PositiveIntegerField(blank = True,null = True)
	content_type = models.ForeignKey(ContentType,blank = True,null = True)	
	confirmation_object = generic.GenericForeignKey('content_type','object_id')
	
	def invalidate(self):
		self.is_valid = False
		self.save()
		
	def is_valid_for(self,function,confirmation_object = None,content_type = None):
		if not self.is_valid or self.function != function:
			return False
		if confirmation_object and self.confirmation_object != confirmation_object:
			return False
		if content_type and self.content_type != content_type:
			return False
		return True
	
	@classmethod
	def has_valid_key_for(cls,email,function,confirmation_object = None):
		try:
			ConfirmationKey.get_valid_key_for(email,function,confirmation_object)
			return True
		except ConfirmationKey.DoesNotExist:
			return False

	@classmethod
	def get_valid_keys_for(cls,email,function,confirmation_object = None):
		if confirmation_object:
			content_type = ContentType.objects.get_for_model(confirmation_object)
			return ConfirmationKey.objects.filter(email = email,function = function,content_type =  content_type,object_id = confirmation_object.id,is_valid = True)
		else:
			return ConfirmationKey.objects.filter(email = email,function = function,is_valid = True)

	@classmethod
	def get_valid_key_for(cls,email,function,confirmation_object = None):
		keys = ConfirmationKey.get_valid_keys_for(email,function,confirmation_object)
		if keys.count() > 1:
			raise ConfirmationKey.MultipleObjectsReturned
		elif keys.count() == 1:
			return keys[0]
		raise ConfirmationKey.DoesNotExist

	@classmethod
	def get_all_valid_keys_for(cls,function,confirmation_object = None):
		if confirmation_object:
			content_type = ContentType.objects.get_for_model(confirmation_object)
			return ConfirmationKey.objects.filter(function = function,content_type =  content_type,object_id = confirmation_object.id,is_valid = True)
		else:
			return ConfirmationKey.objects.filter(function = function,is_valid = True)
	
	def initialize(self,email,function,confirmation_object = None,created_by = None,key_length = 16):
		try:
			key = ConfirmationKey.get_valid_key_for(email,function,confirmation_object)
			if (datetime.datetime.now()-key.created_at) < datetime.timedelta(seconds = global_settings.EMAIL_ACTION_REPEAT_TIME):
				raise ConfirmationKey.TooManyKeysSentRecently
			else:
				key.invalidate()
		except ConfirmationKey.DoesNotExist:
			pass
		self.email = email
		self.function = function
		key_candidate = ''
		while key_candidate == '' or ConfirmationKey.objects.filter(key = key_candidate).count():
			key_candidate = generate_random_key(key_length)
		self.key = key_candidate
		self.is_valid = True
		if created_by:
			self.created_by = created_by
		if confirmation_object != None:
			self.confirmation_object = confirmation_object
		self.has_been_opened = False
		self.status = 0
		self.has_been_sent = False
		self.failed_to_send = False

class Image(Commons):
	user = models.ForeignKey(User,related_name = 'images',blank = True,null = True,default =None,on_delete = models.SET_NULL)
	path = models.CharField(max_length = 255)
	url = models.CharField(max_length = 255)
	accepted = models.BooleanField(default = False)
	rejected = models.BooleanField(default = False)
	width = models.IntegerField(default = -1)
	height = models.IntegerField(default = -1)
	type = models.CharField(max_length = 100,default = '')
	description = models.CharField(max_length = 255,default = '')
	base_image = models.ForeignKey('Image',related_name = 'derived_images',blank = True,null = True)

	reviewer = models.ForeignKey(User,related_name = 'reviewed_images',blank = True,null = True,default = None,on_delete = models.SET_NULL)
	reviewer_comment = models.TextField(default = '')

	@property
	def alternative_versions(self):
		
		class AlternativeVersions:
						
			def __getitem__(self,key):
				image = self._image
				
				def search_image(image,key,images_searched = []):
					if image in images_searched:
						return None
					images_searched.append(image)
					if image.type == key:
						return image
					for derived_image in image.derived_images.all():
						result = search_image(derived_image,key,images_searched)
						if result:
							return result
					return None
				
				while image.base_image != None:
					image = image.base_image
				
				return search_image(image,key)
			
			def __init__(self,image):
				self._image = image
		
		return AlternativeVersions(self)
	
	@property
	def derived_images_dict(self):
		derived_images = {}
		for derived_image in self.derived_images.all():
			derived_images[derived_image.type] = derived_image
		return derived_images
	
	def splitPath(self):
		try:
			matchObject = re.search(r"^(.*)\/([^\/]*)\.(\w+)$",self.path)
			directory = matchObject.group(1)
			basename = matchObject.group(2)
			extension = matchObject.group(3)
		except:
			raise Exception("Cannot determine directory, filename and extension from image path: %s" % self.path)
		return (directory,basename,extension)

	def directory(self):
		return self.splitPath()[0]
	
	def filename(self):
		return self.splitPath()[1]+"."+self.splitPath()[2]
	
	def extension(self):
		return self.splitPath()[2]
	
	def basename(self):
		return self.splitPath()[1]

def _delete_image_from_disk(sender,**kwargs):
	image = kwargs['instance']
	if os.path.exists(image.path) and os.path.isfile(image.path):
		try:
			os.remove(image.path)
			print "Deleted file %s" % image.path
		except:
			print "Could not delete file..."

post_delete.connect(_delete_image_from_disk,sender = Image)

class Profile(Commons):

	class Appearance:
		FULL_NAME = 0
		FIRST_NAME_AND_INITIAL = 1
		LAST_NAME_AND_INITIAL = 2
		USERNAME = 3

	class NotificationPolicy:
		IMMEDIATE = 0
		ONCE_PER_DAY = 1
		ONCE_PER_WEEK = 2
		DONT_NOTIFY_ME = 3
	
	def __unicode__(self):
		return unicode(self.user.email)
		
	@property
	def profile_image_or_placeholder(self):
		if self.profile_image:
			return self.profile_image
		return Image.objects.get(id = settings.PROFILE_IMAGE_PLACEHOLDER_ID)

	profile_image = models.ForeignKey(Image,blank = True,default = None,null = True,related_name = 'profile_photos',on_delete = models.SET_NULL) 
		
	first_name = models.CharField(max_length = 200,default = '')
	last_name = models.CharField(max_length = 200,default = '')
	
	has_verified_name = models.BooleanField(default = False)
	has_verified_email = models.BooleanField(default = False)
	has_beta_key = models.BooleanField(default = False)	
	
	is_active = models.BooleanField(default = True)

	username = models.CharField(max_length=200,default = '',blank = True)

	user = models.OneToOneField(User)

	appearance_on_platform = models.IntegerField(default = Appearance.FIRST_NAME_AND_INITIAL)

	notification_policy = models.IntegerField(default = NotificationPolicy.IMMEDIATE)
	notification_weekday = models.IntegerField(default = 0)
	notification_time = models.TimeField(default = None,blank = True, null = True)
	        
	def screenname(self,appearance = None):
		if not self.is_active:
			return ''
		if appearance == None:
			appearance = self.appearance_on_platform
		if appearance == Profile.Appearance.FULL_NAME and self.last_name and self.first_name:
			name = self.first_name+" "+self.last_name
		elif appearance == Profile.Appearance.FIRST_NAME_AND_INITIAL and self.last_name and self.first_name:
			name = self.first_name+" "+self.last_name[:1]+"."
		elif appearance == Profile.Appearance.LAST_NAME_AND_INITIAL and self.last_name and self.first_name:
			name = self.first_name[:1]+". "+self.last_name
		elif appearance == Profile.Appearance.USERNAME and self.username:
			name = self.username
		else:
			name = "Anonymous"
		return name