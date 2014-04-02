import json
from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView

class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            resp = {'id': request.user.get_username(),
                    'kind': 'debsso#personOpenIdConnect',
                    'sub': request.user.get_username(),
                    'name': request.user.get_full_name(),
                    'given_name': request.user.get_first_name(),
                    'family_name': request.user.get_last_name(),
                    'email': request.user.get_email(),
                    'email_verified': 'true'}
        else:
            # we should never hit the protected API endpoint w/o a user
            resp = {}
        return HttpResponse(json.dumps(resp), content_type="application/json" )
