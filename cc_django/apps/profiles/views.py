# Create your views here.f
# -*- coding: utf-8 -*-

from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _
from django.shortcuts import *
from django.core.urlresolvers import reverse,resolve
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as dlogin
from django.contrib.auth import logout as dlogout
from django.db import IntegrityError
from django.http import *
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType

from profiles.utils.image import *
from profiles.utils.random_keys import *
import profiles.mailer as mailer
import profiles.settings as settings
from profiles.models import Profile
from profiles.forms import *

from functools import wraps
import urllib
import traceback
import datetime
import os.path
import re
import PIL.Image

def _delete_user_profile(profile):
    profile.delete()
        
def _directly_login_user(request,user):
    user.backend = "django.contrib.auth.backends.ModelBackend"
    dlogin(request,user)

def notify_staff(data,notification_object = None):
    admins = User.objects.filter(is_staff = True)
    for admin in admins:
        pass
#	notification = Notification()
#	notification.notification_type = 'general_message'
#	notification.user = admin
#	notification.notification_object = notification_object
#	notification.set_data(data)
#	notification.save()

class logout_first(object):
	
	def __init__(self):
		pass
	
	def __call__(self,function):
		@wraps(function)	
		def logout_first_wrapper(request,*args,**kwargs):
			dlogout(request)
			return function(request,*args,**kwargs)
		return logout_first_wrapper

class logout_if_user_email_does_not_match_key(object):
    
    def __init__(self,key_name):
	self.key_name = key_name
	
    def __call__(self,function):
	    @wraps(function)
	    def logout_if_user_email_does_not_match_key_wrapper(request,**kwargs):
		if request.user.is_authenticated():
		    if not self.key_name in kwargs:
			raise Http404
		    try:
			key = kwargs[self.key_name]
			if "confirmation_key_"+key in request.session:
			    return function(request,**kwargs)
			confirmation_key = ConfirmationKey.objects.get(key = key)
		    except ConfirmationKey.DoesNotExist:
			raise Http404
		    print confirmation_key.email,request.user.email
		    if confirmation_key.email != request.user.email:
			request.flash["notice"] = _(u"You have been logged out.")
			dlogout(request)
			request.session["confirmation_key_"+key] = True
		return function(request,**kwargs)
		    
    	    return logout_if_user_email_does_not_match_key_wrapper
	
class login_required(object):
	
	def __init__(self,staff_required =False):
		self.staff_required = staff_required
	
	def __call__(self,function):
		@wraps(function)
		def check_for_user(request,*args,**kwargs):
			if request.user.is_authenticated() and request.user.profile.is_active and (request.user.is_staff or not self.staff_required):
				return function(request,*args,**kwargs)
			else:
				request.flash['notice'] = _(u"Please log in or sign up first.")
				return redirect('profiles.views.login_or_signup',next_url = request.get_full_path())
		return check_for_user

class betakey_required(object):

	def __init__(self):
		pass
		
	def __call__(self,function):
		@wraps(function)	
		def check_for_betakey(request,*args,**kwargs):
			if (not request.user.is_authenticated() or not (request.user.profile.has_beta_key or request.user.is_staff)) and not settings.IGNORE_MISSING_BETA_KEY:
			    csrfContext = RequestContext(request)
			    context = Context({})
			    return render_to_response('beta_notice.html', context,csrfContext)
			else:
				return function(request,*args,**kwargs)
		return check_for_betakey

def logout_and_goto(request,url):
    if request.user.is_authenticated():
	dlogout(request)
    if url[0] != "/":
	raise Http404
    return redirect(url)

def exception_test(request):
    print settings.DEBUG
    raise Exception("This is just a test exception, please feel free to ignore it (btw, nuclear core meltdown is imminent).")

@login_required()
@csrf_protect
def change_name(request):
	csrfContext = RequestContext(request)
	profile = request.user.profile
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			if form.cleaned_data["first_name"] == profile.first_name and form.cleaned_data["last_name"] == profile.last_name:
				request.flash["notice"] = _(u"Your name has not been changed.")
				return redirect(profile_settings)
			profile.first_name = form.cleaned_data["first_name"].strip()
			profile.last_name = form.cleaned_data["last_name"].strip()
			profile.save()
			profile.user.save()
			request.flash["notice"] = _(u"Yout name has been changed.")
			return redirect(profile_settings)
		else:
			request.flash.now["error"] = _(u"Please correct the indicated errors.")
	else:
		form = NameForm(initial = {'first_name':profile.first_name,'last_name':profile.last_name})
	context = Context({'form':form})
	return render_to_response('profiles/change_name.html', context,csrfContext)

@login_required()
@csrf_protect
def change_username(request):
	csrfContext = RequestContext(request)
	profile = request.user.profile
	if request.method == 'POST':
		form = ChangeUsernameForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			if Profile.objects.filter(username = username).exclude(user = request.user).count():
			    request.flash.now["error"] = _(u"This username does already exist.")
			else:
			    profile.username = username.strip()
			    profile.save()
			    request.flash["notice"] = _(u"Your username has been changed.")
			    return redirect(profile_settings)
		else:
			request.flash.now["error"] = _(u"Please correct the indicated errors.")
	else:
		form = ChangeUsernameForm(initial = {'username':profile.username})
	context = Context({'form':form})
	return render_to_response('profiles/change_username.html', context,csrfContext)

@login_required()
@csrf_protect
def profile_settings(request):
	csrfContext = RequestContext(request)
	try:
		profile = request.user.profile
	except Profile.DoesNotExist:
		request.user.profile = Profile()
		request.user.profile.save()
		request.user.save()
		profile = request.user.profile
	if request.method == 'POST':
		form = SettingsForm(request.POST)
		if form.is_valid():
			for key in ["notification_policy","appearance_on_platform"]:
				setattr(profile,key,form.cleaned_data[key])
			profile.save()
			profile.user.save()
			request.flash["notice"] = _(u"Your settings have been saved.")
			return redirect(profile_settings)
		else:
			request.flash.now["error"] = _(u"Please correct the indicated errors.")
	else:
		form = SettingsForm(initial = {'first_name':profile.first_name,'last_name':profile.last_name,'notification_policy':profile.notification_policy,'appearance_on_platform':profile.appearance_on_platform})
	
	notification_policy = profile.notification_policy
	appearance_on_platform = profile.appearance_on_platform
		
	context = Context({'form':form,'notification_policy':notification_policy,'appearance_on_platform':appearance_on_platform})
	return render_to_response('profiles/profile_settings.html', context,csrfContext)

@csrf_protect
def logout(request):
	if request.user.is_authenticated:
		dlogout(request)
		request.flash['notice'] = _(u"You have been signed out.")
		if "chamaeleon_user" in request.session:
			del request.session["chamaeleon_user"]
	return redirect('profiles.views.login')		
    
@csrf_protect
@login_required()
def remove_profile_image(request):
	csrfContext = RequestContext(request)
	profile = request.user.profile
	if profile.profile_image:
		profile.profile_image.base_image.base_image.delete()
	request.flash["notice"] = _(u"Your profile photo has been removed.")
	return redirect(change_profile_image)

@csrf_protect
@login_required()
def change_profile_image_clipping(request):
	csrfContext = RequestContext(request)
	if not request.user.profile.profile_image.base_image:
		request.flash["error"] = _(u"You didn't upload a profile photo.")
		return redirect(change_profile_image)
	if request.method == 'POST':
		form = ChangeProfileImageClippingForm(request.POST)
		if form.is_valid():
			try:
				profile = request.user.profile

				original_image = profile.profile_image.base_image.base_image

				base_image = profile.profile_image.base_image

				w = base_image.width
				h = base_image.height
				
				dw = settings.PROFILE_IMAGE_DIMENSIONS[0]
				dh = settings.PROFILE_IMAGE_DIMENSIONS[1]
				if w > h:
					positions = ((0,0),(int((w-dw)/2),0),((w-dw),0))
				else:
					positions = ((0,0),(0,int((h-dh)/2)),(0,(h-dh)))
				profile.profile_image.delete()
				(profileImage,profileImageBase,profileImageSmall,profileImageThumbnail) = rescale_and_crop_image(original_image,position = positions[int(form.cleaned_data["clipping_position"])-1])
				profile.profile_image = profileImage
				profile.save()
								
				request.flash["notice"] = _(u"Your photo has been rescaled.")
			except:
				traceback.print_exc()
				request.flash["error"] = _(u"Rescaling failed, sorry.")
			return redirect(change_profile_image)
		else:
			request.flash["error"] = _(u"Please select a rescaling option.")
			return redirect(change_profile_image)
	return redirect(change_profile_image)

@csrf_protect
@login_required()
def change_profile_image(request):
    csrfContext = RequestContext(request)
    if request.method == 'POST':
	    form = UploadImageForm(request.POST,request.FILES)
	    if form.is_valid():
		    try:
			    try:
				image = upload_image(form.cleaned_data["image"],request.user)
				profile = request.user.profile
				
				(profileImage,profileImageCover,profileImageSmall,profileImageThumbnail) = rescale_and_crop_image(image)
				
				profile.profile_image = profileImage
				profile.save()
				
				request.flash["notice"] = _(u"Your profile photo has been uploaded.")
				return redirect(change_profile_image)
			    except AspectRatioException:
				request.flash.now["error"] = _u("Please make sure that the aspect ratio of your photo is at least %g" % (settings.IMAGE_MINIMUM_ASPECT_RATIO))

		    except:
			    traceback.print_exc()
			    request.flash.now["error"] = _(u"We could not upload your photo, sorry.")
	    else:
		    request.flash.now["error"] = _(u"Please correct the indicated errors.")
    else:
	    form = UploadImageForm()
    original_image = {}
    profile = request.user.profile

    if profile.profile_image and profile.profile_image.base_image:
	    
	    base_image = profile.profile_image.base_image
	    
	    factor = 2
	    
	    original_image["width"] = base_image.width
	    original_image["height"] = base_image.height
	    original_image["desired_width"] = settings.PROFILE_IMAGE_DIMENSIONS[0]
	    original_image["desired_height"] = settings.PROFILE_IMAGE_DIMENSIONS[1]
	    original_image["desired_width_display"] = settings.PROFILE_IMAGE_DIMENSIONS[0]/factor
	    original_image["desired_height_display"] = settings.PROFILE_IMAGE_DIMENSIONS[0]/factor
	    w = base_image.width
	    h = base_image.height
	    
	    original_image["original_width_display"] = w/factor
	    original_image["original_height_display"] = h/factor
	    
	    dw = settings.PROFILE_IMAGE_DIMENSIONS[0]
	    dh = settings.PROFILE_IMAGE_DIMENSIONS[1]
	    if w > h:
		    original_image["positions"] = (0,-int((w-dw)/2)/factor,-(w-dw)/factor)
		    original_image["position_name"] = "left"
	    else:
		    original_image["positions"] = (0,-int((h-dh)/2)/factor,-(h-dh)/factor)
		    original_image["position_name"] = "top"

    return render_to_response('profiles/change_profile_image.html',{'form_url':reverse('profiles.views.change_profile_image'),'form':form,'original_image':original_image},csrfContext)
	
@csrf_protect
def activate_account(request,account_activation_key = None):
    csrfContext = RequestContext(request)
    try:
	key = ConfirmationKey.objects.get(key = account_activation_key,function = 'signup')
    except ConfirmationKey.DoesNotExist:
	request.flash["error"] = _(u"The supplied key does not exist.")
	raise Http404
    if not key.is_valid:
	return render_to_response('information.html',{'title':_(u"User account already activated"),'text':_(u"It seems that your user account has already been activated.")},csrfContext)
    if User.objects.filter(email = key.email,profile__isnull = False).count():
	return render_to_response('information.html',{'title':_(u"A user with this e-mail address already exists."),'text':_(u"We are sorry, but the e-mail address you have chosen is already associated to a user account.")},csrfContext)
    else:
	data = key.get_data()
	user = User()
	profile = Profile()

	obsolete_users = User.objects.filter(email = key.email)

	for obsolete_user in obsolete_users:
	    obsolete_user.email = ''
	    obsolete_user.save()

	user.username = generate_random_key()
	user.email = key.email
	user.set_password(data["password"])

	notify_staff({'title':'New user account','text':"Somebody with email %s has created a new user account." % key.email},notification_object = user)

	user.save()

	profile.user = user
	profile.has_verified_email = True
	profile.is_active = True
	profile.has_beta_key = True

	profile.save()
	
	#We remove the sensitive password from the key's data.
	del data["password"]
	key.set_data(data)
	key.invalidate()
	

	_directly_login_user(request,profile.user)

	csrfContext = RequestContext(request)
	next_url = None
	if 'next_url' in data:
	    next_url = data['next_url']
	return render_to_response('profiles/activate_account.html', {'next_url':next_url},csrfContext)

@csrf_protect
def change_email(request,email_change_key):
    try:
        key = ConfirmationKey.objects.get(key = email_change_key,function = "email_change",is_valid = True)
    except ConfirmationKey.DoesNotExist:
	request.flash["error"] = _(u"Key not found!")
	raise Http404
    user = key.created_by
    email = key.email
    key.invalidate()
    _directly_login_user(request,user)
    csrfContext = RequestContext(request)
    if User.objects.filter(email = email).count():
	request.flash["error"] = _(u'We cannot change your e-mail to the address you requested since it is already in our database.')
    else:
	user.email = email
	user.save()
	user.profile.has_verified_email = True
	user.profile.save()
	request.flash["notice"] = _(u'Thanks, your e-mail has been changed to %s.' % user.email)
    return redirect(profile)

@logout_first()
def delete_account(request,account_deletion_key = None):
    csrfContext = RequestContext(request)
    try:
        key = ConfirmationKey.objects.get(key = account_deletion_key,function = "account_deletion",is_valid = True)
    except ConfirmationKey.DoesNotExist:
	request.flash["error"] = _(u"Key not found!")
	raise Http404
    try:
	user = User.objects.get(email = key.email)
    except User.DoesNotExist:
	raise Http404
    _delete_user_profile(user.profile)
    key.invalidate()
    return render_to_response('information.html',{'title':u'Account deleted.','text':_(u'Your account %s has been deleted. Farewell!' % user.email)},csrfContext)

@csrf_protect
@logout_first()
def reset_password(request,password_reset_key = None):
    csrfContext = RequestContext(request)
    try:
        key = ConfirmationKey.objects.get(key = password_reset_key,function = "password_reset",is_valid = True)
    except ConfirmationKey.DoesNotExist:
	request.flash["error"] = _(u"Key not found!")
	raise Http404
    try:
        user = User.objects.get(email = key.email)
    except User.DoesNotExist:
	raise Http404
    request.flash["notice"] = _(u"Please choose a password:")
    _directly_login_user(request,user)
    key.invalidate()
    return redirect(change_password)

@csrf_protect
@login_required()
def request_email_change_key(request):
    csrfContext = RequestContext(request)
    if request.method == 'POST':
	form = EmailChangeForm(request.POST)
	if form.is_valid():
	    email = form.cleaned_data["email"]
            users = User.objects.filter(email = email)
            if users.count():
                request.flash.now["error"] = _(u"Account with that e-mail already exists.")
            else:
                key = ConfirmationKey()
                try:
                    key.initialize(email = email,function = "email_change",created_by = request.user)
                    key.set_data({'email':email})
                    key.save()
                    mailer.send_confirmation_email.delay(key.id)
                    request.flash["notice"]= _(u"We have send you a confirmation e-mail with further instructions.")
                except ConfirmationKey.KeyError:
                    request.flash["error"] = _(u"An error occured, sorry.")
            return redirect(profile_settings)
	else:
	    request.flash.now["error"] = _(u"Please correct the indicated errors.")
    else:
	form = EmailChangeForm()
    return render_to_response('profiles/request_email_change_key.html',{'form':form},csrfContext)

@login_required()
@csrf_protect
def change_password(request):
    csrfContext = RequestContext(request)
    if request.method == 'POST':
	form = ChangePasswordForm(request.POST)
	if form.is_valid():
	    if form.cleaned_data["new_password"] != form.cleaned_data["new_password_confirmed"]:
		request.flash.now["error"] = _(u"Passwords do not match.")
	    else:
		request.user.set_password(form.cleaned_data["new_password"])
		request.user.save()
		request.flash["notice"] = _(u"Your password has been changed.")
		return redirect(profile_settings)
    else:
	form = ChangePasswordForm()
    return render_to_response('profiles/change_password.html',{'form':form},csrfContext)

@csrf_protect
def request_access_key(request,email = None):
    csrfContext = RequestContext(request)
    if request.method == 'POST' or email:
	if request.method == 'POST':
		form = RequestAccessKeyForm(request.POST)
	else:
		form = RequestAccessKeyForm(initial = {'email':email})
	if form.is_valid():
	    email = form.cleaned_data["email"]
	    try:
		user = User.objects.get(email = email)
	    except User.DoesNotExist:
		request.flash.now["error"] = _(u"This e-mail address is unknown.")
		raise Http404
	    except User.MultipleObjectsReturned:
		raise PermissionDenied
	    key = ConfirmationKey()
	    try:
		key.initialize(email = user.email,function = 'access_key',created_by = user)
		key.save()
                mailer.send_confirmation_email.delay(key.id)
	    except ConfirmationKey.KeyError:
		request.flash["error"] = _(u"An error occured, sorry.")
		return redirect(request_access_key,email = email)
	    request.flash["notice"]= _(u"We have send you an e-mail with further instructions.")
	    return redirect(login)
    else:
	form = RequestAccessKeyForm()
    return render_to_response('profiles/request_access_key.html',{'form':form},csrfContext)

@logout_first()
def login_with_access_key(request,access_key):
    try:
	key = ConfirmationKey.objects.get(key = access_key,function = 'access_key',is_valid = True)
    except ConfirmationKey.DoesNotExist:
	request.flash["error"] = _(u"Invalid access key")
	raise Http404
    try:
	user = User.objects.get(email = key.email)
    except User.DoesNotExist:
	raise Http404
    _directly_login_user(request,user)
    return redirect(change_password)

@csrf_protect
def resend_account_activation_key(request,email = None):
    csrfContext = RequestContext(request)
    if request.method == 'POST':
	    form = RequestAccountActivationKeyForm(request.POST)
    if form.is_valid():
	email = form.cleaned_data["email"]
	try:
#	    key = ConfirmationKey.objects.get(email = email,function = 'signup')
	    return render_to_response('information.html',{'title':u'E-Mail has been sent.','text':_(u'We just sent you an e-mail with further instructions.')},csrfContext)
	except ConfirmationKey.DoesNotExist:
	    request.flash.now["error"] = _(u"The e-mail address you supplied is unknown.")
    else:
	form = RequestAccountActivationKeyForm(initial = {'email':email})
    return render_to_response('profiles/resend_account_activation_key.html',{'form':form},csrfContext)

#Sign up for a real user account...
@logout_first()
@csrf_protect
def signup(request,next_url = ''):
    if request.method == 'POST':
	    form = SignupForm(request.POST)
	    if form.is_valid():
		data = form.cleaned_data
		email = data["email"]
		data['next_url'] = next_url
		try:
		    key = ConfirmationKey()
		    key.initialize(function = 'signup',email = email)
		    key.set_data(data)
		    key.save()
		    if settings.CONFIRM_SIGNUP_BY_ADMIN:
			notify_staff({'title':u'New account created','text':u"A new user account with e-mail %s has been created. Please confirm.\n\n%s" % (email,'')},notification_object = key)
			request.flash["notice"] = _(u"Thanks, we have saved your request.")
		    else:
                        mailer.send_confirmation_email.delay(key.id)
		    return redirect(reverse('profiles_signup_next_steps'))
		except ConfirmationKey.KeyError:
		    request.flash.now["error"] = _(u"An error occured, sorry.")
	    else:
		request.flash.now["error"] = _(u"Please correct the indicated errors.")
    else:
	form = SignupForm()
    csrfContext = RequestContext(request)
    return render_to_response('profiles/signup.html', {'form': form,'next_url':next_url},csrfContext)

@csrf_protect
@login_required()
def request_account_deletion_key(request):

    if not 'confirmed' in request.GET:
	    return ask_question(request,question = _(u"Do you really want to delete your account?"),
				yesText = _(u"Yes"),
				yes = (reverse('profiles.views.request_account_deletion_key',args=[])+"?confirmed=1"),
				noText = _(u"No"),
				no = reverse('profiles.views.profile_settings',args=[])
				)
    key = ConfirmationKey()
    try:
	key.initialize(email = request.user.email,function = "account_deletion",created_by = request.user)
	key.save()
        mailer.send_confirmation_email.delay(key.id)
    except ConfirmationKey.KeyError:
	request.flash["error"] = _(u"An error occured, sorry.")
    return redirect(reverse('profiles_account_deletion_key_sent'))

@betakey_required()
def profile(request,user_id = None):

	csrfContext = RequestContext(request)
	
	if user_id == None:
	    if request.user.is_authenticated():
		user = request.user
	else:
	    try:
		user = User.objects.get(id = user_id)
	    except User.DoesNotExist:
		request.flash.now["error"] = _(u"Invalid username")
		raise Http404

	return render_to_response('profiles/profile.html',{'profile_user':user,
							}
				  ,csrfContext)

def login_or_signup(request,next_url = ''):
    login_form = LoginForm()    
    signup_form = SignupForm()    
    context = RequestContext(request)
    return render_to_response('profiles/login_or_signup.html',{'signup_form':signup_form,'login_form':login_form,'next_url':next_url},context)
    
@csrf_protect
def login(request,email = None,next_url = ''):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			users = User.objects.filter(email = email,profile__isnull = False)
			if users.count():
				user = users[0]
				if not user.profile.is_active:
					request.flash.now["error"] = _(u"Your account is not active.")
				else:
					user = authenticate(username=user.username,password=password)
					if user is not None:
						dlogin(request,user)
						request.flash["notice"] = _(u"You are logged in now!")
						if next_url != '':
							if next_url[0] != "/":
							    raise Http404
							else:
							    return redirect(next_url)
						else:
							return redirect(reverse(settings.DEFAULT_URL_AFTER_LOGIN))
					else:
						request.flash.now["error"] = _(u"Wrong password, please try again.")

			else:
				request.flash["error"] = _(u"Unknown e-mail address.")
		else:
			request.flash.now["error"] = _(u"Please indicate your e-mail and password.")
	else:
		form = LoginForm(initial = {'email':email})
	context = RequestContext(request)
	return render_to_response('profiles/login.html',{'form':form,'next_url':next_url},context)

"""
ADMIN views
"""

@login_required(staff_required = True)
def send_activation_key(request,key_id):
    try:
	mailer.send_confirmation_email.delay(key_id)
    except:
	request.flash["error"] = _(u"An error occured, sorry.")
    request.flash["notice"] = _(u"Activation key has been sent.")
    return redirect(profile)

@login_required(staff_required = True)
def delete_activation_key(request,key_id):
    try:
	key = ConfirmationKey.objects.get(id = key_id)
    except ConfirmationKey.DoesNotExist:
	raise Http404
    if not 'confirmed' in request.GET:
	    return ask_question(request,question = _(u"Really delete activation key?"),
				yesText = _(u"Yes") ,
				yes = (reverse('profiles.views.delete_activation_key',args=[key.id])+"?confirmed=1"),
				noText = _(u"No"),
				no = reverse('profiles.views.profile'))
    else:
	key.delete()
    request.flash["notice"] = _(u"Activation key has been deleted.")
    return redirect(profile)

@login_required(staff_required = False)
@csrf_protect
def change_chamaeleon_username(request):
	if hasattr(request,'chamaeleon_user'):
		user = request.chamaeleon_user
	else:
		user = request.user
	if not user.is_staff:
	    request.flash.now["error"] = _(u"You are not authorized to use this function.")
	    raise PermissionDenied
	if not request.method == 'POST':
		request.flash["error"] = _("You must supply a username.")
		return redirect(settings.DEFAULT_URL_AFTER_LOGIN)
	else:
		if request.POST['username'] != '':
			request.session['chamaeleon_user'] = int(request.POST['username'])
			request.flash["notice"] = _("Your identity has been changed.")
		elif 'chamaeleon_user' in request.session:
			request.flash["notice"] = _("Your identity has been reset.")
			del request.session['chamaeleon_user']
		if 'next_url' in request.POST:
			return redirect(request.POST['next_url'])
		else:
			return redirect(settings.DEFAULT_URL_AFTER_LOGIN)
