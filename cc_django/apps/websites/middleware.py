from django.utils.translation import ugettext as _
import websites.models as models

class WebsiteAdminMiddleware(object):
    
    def process_request(self,request):
        if request.user.is_authenticated():
            user_websites = request.user.website_admins.all() | request.user.website_owners.all()
            request.user_websites = user_websites
        return None

class ActiveWebsiteMiddleware(object):
    
    def process_request(self,request):
        if 'active_website_id' in request.session:
            try:
                website = models.Website.objects.get(id = request.session['active_website_id'])
                if request.user.is_authenticated and (request.user in website.admins.all() or request.user in website.owners.all() or request.user.is_staff):
                    request.active_website = website
            except:
                del request.session['active_website_id']
        if request.user.is_authenticated():
            user_websites = request.user.website_admins.all() | request.user.website_owners.all()
            request.user_websites = user_websites
            if not 'active_website_id' in request.session:
                request.session['active_website_id'] = request.user_websites[0].id
        return None