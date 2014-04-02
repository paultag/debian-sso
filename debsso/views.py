
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import json
from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView

def _dump_args(request, tag):
    pass
    import datetime, os
    now = datetime.datetime.utcnow()
    with open("/tmp/sso-log-" + tag, "at") as fd:
        os.fchmod(fd.fileno(), 0640)
        print("--- {}".format(now.strftime("%Y-%m-%d %H:%M:%S")), file=fd)
        for k, v in request.GET.iteritems():
            print("GET {} -> {}".format(k, v), file=fd)
        for k, v in request.POST.iteritems():
            print("POST {} -> {}".format(k, v), file=fd)
        for k, v in request.environ.iteritems():
            print("ENV {} -> {}".format(k, v), file=fd)
        for k, v in request.COOKIES.iteritems():
            print("COOKIE {} -> {}".format(k, v), file=fd)

class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        if request.resource_owner:
            user = request.resource_owner
#            scopes = request.scopes
#            resp = {}
#            if "openid" in scopes:
#                resp['id'] = request.user.get_username()
#                resp['kind'] = "debsso#personOpenIdConnect"
#                resp['sub'] = request.user.get_username()
#                resp['name'] = request.user.get_full_name()
#                resp['given_name'] = request.user.get_first_name()
#                resp['family_name'] = request.user.get_last_name()
#            if "email" in scopes:
#                resp['email'] = request.user.get_email()
#                resp['email_verified'] = "true"
#            if "profile" in scopes:
#                resp['provider'] = request.user.get_provider()
            resp = {'id': user.get_username(),
                    'kind': 'debsso#personOpenIdConnect',
                    'sub': user.get_username(),
                    'name': user.get_full_name(),
                    'given_name': user.get_first_name(),
                    'family_name': user.get_last_name(),
                    'email': request.resource_owner.email,
                    'email_verified': 'true'}
        else:
            # we should never hit the protected API endpoint w/o a user
            resp = {}
        return HttpResponse(json.dumps(resp), content_type="application/json" )
