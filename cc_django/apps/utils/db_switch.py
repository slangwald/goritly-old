from cc_django.middleware import *
from cc_django.apps.global_settings import UTILS_DATABASE
import sys
class UserDBRouter(object):
    
    """
    A router to control all database operations on models in the
    auth application.
    """

    def get_active_website(self):
        # Command from CLI
        if UTILS_DATABASE != None:
            return UTILS_DATABASE
        
        active_website_id = get_session().get('active_website_id')
        active_website = 'website_' + str(active_website_id)
        return active_website

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'utils':
            active_website = self.get_active_website()
            return active_website
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'utils':
            active_website = self.get_active_website()
            return active_website
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'utils' or \
           obj2._meta.app_label == 'utils':
           return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db == 'utils_db':
            return model._meta.app_label == 'auth'
        elif model._meta.app_label == 'auth':
            return False
        return None