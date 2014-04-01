import json
from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView

class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        resp = {'id': 'zobel', 'kind': 'debsso#personOpenIdConnect', 'gender': 'male', 'sub': 'zobel', 'name': 'Martin Zobel-Helas', 'given_name': 'Martin', 'family_name': 'Zobel-Helas', 'email': 'zobel@debian.org', 'email_verified': 'true'}
        return HttpResponse(json.dumps(resp), content_type="application/json" )
