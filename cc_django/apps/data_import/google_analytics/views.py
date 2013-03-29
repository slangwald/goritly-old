import os
import logging
import httplib2
import datetime

from apiclient.discovery import build
from profiles.views import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,redirect
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets,AccessTokenRefreshError
from oauth2client.django_orm import Storage
from django.template import Context, loader, RequestContext

from data_import.google_analytics.models import CredentialsModel
from data_import.google_analytics import settings
from websites.views import valid_website_required
# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/analytics.readonly',
    redirect_uri='http://gpsfront.cleansy.org:5000/import/google_analytics/auth_return')
FLOW.params['approval_prompt'] = 'force'

@login_required()
@valid_website_required()
def index(request):
    try:
      credentialsModel = CredentialsModel.objects.get(website = request.active_website)
      credential = credentialsModel.credential
    except CredentialsModel.DoesNotExist:
      credential = None
    print credential,request.active_website.id
    try:
        if credential is None or credential.invalid == True:
            FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                     request.active_website)
            authorize_url = FLOW.step1_get_authorize_url()
            return HttpResponseRedirect(authorize_url)
        else:
            http = httplib2.Http()
            http = credential.authorize(http)
            service = build("analytics", "v3", http=http)
            accounts = service.management().accounts().list().execute()
            profiles = service.management().profiles().list(accountId = '~all',webPropertyId = '~all').execute()
            print profiles
            start_date = datetime.datetime.today().date()-datetime.timedelta(days = 30)
            end_date = datetime.datetime.today().date()
            data = service.data().ga().get(start_date = start_date.strftime("%Y-%m-%d"),end_date = end_date.strftime("%Y-%m-%d"), ids = 'ga:'+profiles['items'][0]['id'],metrics = 'ga:visits',dimensions = 'ga:browser,ga:city').execute()
            print data
            logging.info(accounts)
            context = RequestContext(request,{
                  'accounts': accounts,
                  })
            return render_to_response('google_analytics/index.html', context)
    except AccessTokenRefreshError:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                 request.active_website)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
        
@login_required()
@valid_website_required()
def auth_return(request):
  if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
                                 request.active_website):
    return  HttpResponseBadRequest()
  credential = FLOW.step2_exchange(request.REQUEST)
  try:
    credentialsModel = CredentialsModel.objects.get(website = request.active_website)
  except CredentialsModel.DoesNotExist:
    credentialsModel = CredentialsModel(website = request.active_website)
  credentialsModel.credential = credential
  credentialsModel.save()
  return redirect(index)
