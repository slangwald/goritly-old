# -*- coding: utf-8 -*-
import json
import datetime
import traceback
from celery.task import task

import django.utils.translation
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader, RequestContext
from django.template.loader import get_template
from django.core.cache import cache

import global_settings as settings
import profiles.models as models


def send_email(to_address,template_path = None,context = {},simulate = False):
    
    if not "server_url" in context:
        context["server_url"] = settings.EMAIL_SERVER_URL
    
    if template_path != None:
        email_template = get_template(template_path)
        render_context = Context(context)
        email_template.render(render_context)
        
    text_content = ""
    html_content = ""
    subject = ""
    
    if "text_content" in render_context :
        text_content = render_context["text_content"]
    if "html_content" in render_context:
        html_content = render_context["html_content"]
    if "subject" in render_context:
        subject = render_context["subject"]

    if simulate:
        return (subject,text_content,html_content)
    
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_INFO_FROM_ADDRESS, [to_address])
    
    
    if html_content:
        msg.attach_alternative(html_content, "text/html")
    
    return msg.send()
    
templatePaths = {
    'signup': "profiles/emails/signup.multipart",
    'email_change': "profiles/emails/request_email_change_key.multipart",
    'access_key': "profiles/emails/request_access_key.multipart",
    'password_reset': "profiles/emails/request_password_reset_key.multipart",
    'account_deletion' : "profiles/emails/request_account_deletion_key.multipart"    
}

class ConfirmationMailException(Exception):
    pass

@task
def send_confirmation_email(key_id):
    key = models.ConfirmationKey.objects.get(id = key_id)
    if not key.function in templatePaths:
        key.has_been_sent = False
        key.failed_to_send = True
        key.save()
        raise ConfirmationMailException("Cannot find template for key function: %s (key id = %d)" % (key.function,key.id))
    try:
        if key.has_been_sent:
            print "Confirmation mail has already been sent, skipping..."
            return
        key.sent_at = datetime.datetime.now()
        key.has_been_sent = True
        key.save()
        send_email(key.email,template_path = templatePaths[key.function],context= {'key':key})
    except:
        print "Unable to send confirmation message!"
        traceback.print_exc()
        key.has_been_sent = False
        key.failed_to_send = True
        key.save()
