# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse,resolve
import django.core.validators as validators
from django.utils.translation import ugettext as _
from profiles.models import *

class UploadImageForm(forms.Form):
    image  = forms.ImageField()

class ChangeProfileImageClippingForm(forms.Form):
    clipping_position = forms.ChoiceField(((1,'1'),(2,'2'),(3,'3')))
    
class SignupForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField( widget=forms.PasswordInput, label="Password" )
    accepted_terms = forms.BooleanField()
    
    def clean(self):
        cleaned_data = self.cleaned_data
	if 'email' in cleaned_data:
	    email = cleaned_data['email']
	    users = User.objects.filter(email = email,profile__isnull = False)
	    if users.count():
		self._errors["email"] = self.error_class([_(u"This e-mail address is already in use.")])
		del cleaned_data["email"]
        return cleaned_data

class RequestPasswordResetForm(forms.Form):
    email = forms.EmailField()

class RequestAccountActivationKeyForm(forms.Form):
    email = forms.EmailField()

class EmailChangeForm(forms.Form):
    email = forms.EmailField()

class RequestAccessKeyForm(forms.Form):
    email = forms.EmailField()

class ChangePasswordForm(forms.Form):
    new_password = forms.CharField( widget=forms.PasswordInput, label=_(u"New password") )
    new_password_confirmed = forms.CharField( widget=forms.PasswordInput, label=_(u"Confirm new password") )

class AccountDeletionForm(forms.Form):
    confirm_deletion = forms.BooleanField(initial = False)

class ChamaeleonUserForm(forms.Form):
	username = forms.ModelChoiceField(queryset = Profile.objects.filter(user__isnull = False))

class AccessKeyLoginForm(forms.Form):
    next_url = forms.CharField(widget=forms.HiddenInput(),label = '',required = False)
    access_key = forms.CharField()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField( widget=forms.PasswordInput, label="Password" )

class SettingsForm(forms.Form):
    appearance_on_platform = forms.ChoiceField(choices = ((Profile.Appearance.USERNAME,u'Username'),(Profile.Appearance.FIRST_NAME_AND_INITIAL,u'Given name and initial'),(Profile.Appearance.LAST_NAME_AND_INITIAL,u'Family name and initial'),(Profile.Appearance.FULL_NAME,u'Full name')),widget=forms.RadioSelect())
    notification_policy = forms.ChoiceField(choices = ((Profile.NotificationPolicy.IMMEDIATE,u'Immediately notify me of important updates.'),(Profile.NotificationPolicy.DONT_NOTIFY_ME,u'Don\'t send me notifications.')), widget=forms.RadioSelect())

class NameForm(forms.Form):
	first_name = forms.CharField(max_length = 100, label =_("Vorname"))
	last_name = forms.CharField(max_length = 100, label =_("Nachname"))

class ChangeUsernameForm(forms.Form):
    username = forms.RegexField(regex = r'^[a-zA-Z0-9]+$',max_length = 20, label =_("Username"),error_messages = {'invalid':_(u"Maximum 20 alphanumeric characters.")})
