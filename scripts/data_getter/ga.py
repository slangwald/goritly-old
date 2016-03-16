#!/usr/bin/env python

import sys, os, httplib2

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+"/../../"))

from apiclient.discovery import build
from oauth2client import client
from oauth2client.client import OAuth2Credentials
from oauth2client.anyjson import simplejson
import mongobean.orm as orm
import cc_django.apps.utils.models as models

models.orm.default_db = models.orm.pymongo.MongoClient()['analytics'] 

class Webproperties(orm.Document):
    pass
class Token(orm.Document):
    pass

webproperty = Webproperties.collection.find_one({'user_id':8})
print webproperty

json = Token.collection.find_one({'user_id':8})['token']

token = simplejson.loads(json)
token['client_id'] = "295121445037.apps.googleusercontent.com"
token['client_secret'] = "<CLIENT SECRET>"
#access_token, client_id, client_secret, refresh_token,
# token_expiry, token_uri, user_agent,
credentials = OAuth2Credentials(access_token = token['access_token'], 
                                client_id = token['client_id'],
                                client_secret = token['client_secret'],
                                refresh_token = token['refresh_token'],
                                token_expiry = token['expires_in'],
                                token_uri = "https://accounts.google.com/o/oauth2/token",
                                user_agent = None)
http = httplib2.Http()
http = credentials.authorize(http)

service = build("analytics", "v3", http=http)



def get_api_query(service):
  """Returns a query object to retrieve data from the Core Reporting API.

  Args:
    service: The service object built by the Google API Python client library.
  """
  return service.data().ga().get(
      ids='ga:69065200',
      start_date='2012-01-01',
      end_date='2013-05-15',
      metrics='ga:visits',
      dimensions='ga:source,ga:keyword',
      sort='-ga:visits',
      #filters='ga:medium==organic',
      start_index='1',
      max_results='25')

profiles = service.management().profiles().list(
          accountId=webproperty['website']['account_id'],
          webPropertyId=webproperty['website']['id']).execute()
print profiles
result = get_api_query(service).execute()
print(result)
