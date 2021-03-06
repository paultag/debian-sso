# coding: utf8
# Debian Single Signon front-end
#
# Copyright (C) 2014  Enrico Zini <enrico@debian.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from urllib import urlencode
import json

def _dump_args(request, tag):
    pass
    # import datetime, os
    # now = datetime.datetime.utcnow()
    # with open("/tmp/sso-log-" + tag, "at") as fd:
    #     os.fchmod(fd.fileno(), 0640)
    #     print("--- {}".format(now.strftime("%Y-%m-%d %H:%M:%S")), file=fd)
    #     for k, v in request.GET.iteritems():
    #         print("GET {} -> {}".format(k, v), file=fd)
    #     for k, v in request.environ.iteritems():
    #         print("ENV {} -> {}".format(k, v), file=fd)
    #     for k, v in request.COOKIES.iteritems():
    #         print("COOKIE {} -> {}".format(k, v), file=fd)

def make_auth_transfer_response(target_federation, dacs_identity, next_url):
    return redirect("https://sso.debian.org/cgi-bin/dacs/dacs_auth_transfer?" + urlencode({
        "OPERATION": "EXPORT",
        "TARGET_FEDERATION": target_federation,
        "DACS_IDENTITY": dacs_identity,
        "TRANSFER_SUCCESS_URL": next_url,
    }))

def acs_error(request):
    """
    Access denied / login required page
    """
    from .dacs_codes import error_for_code
    _dump_args(request, "acs_error")
    dacs_user = request.environ.get("DACS_USERNAME", None)
    next_federation = request.GET.get("DACS_FEDERATION", None)
    next_url = request.GET.get("DACS_ERROR_URL", None)

    if dacs_user is not None and next_url is not None \
       and request.GET.get("DACS_ERROR_CODE", None) == "902" \
       and next_federation != "DEBIANORG":
        # ACS error because someone who is logged on SSO tried to access a
        # restricted page on a federation where auth has not been trasnfedered
        # yet. Trigger auth transfer.
        return make_auth_transfer_response(next_federation, request.environ["DACS_IDENTITY"], next_url)

    return render(request, "sso/login.html", {
        "dacs_error": error_for_code(request.GET.get("DACS_ERROR_CODE", None)),
        "dacs_error_url": request.GET.get("DACS_ERROR_URL"),
        "next_url": next_url,
    })

def login_error(request):
    """
    Error posting login info
    """
    from .dacs_codes import error_for_code
    _dump_args(request, "login_error")
    next_url = request.GET.get("DACS_AUTH_SUCCESS_HANDLER", None)
#        if ( $c->req->param('DACS_ERROR_URL') ) {
#                $c->stash->{DACS_ERROR_URL} = $tf->filter($c->req->param('DACS_ERROR_URL'));
#        }
    return render(request, "sso/login.html", {
        "dacs_error": error_for_code(request.GET.get("DACS_ERROR_CODE", None)),
        "next_url": next_url,
    })

def login(request):
    """
    Plain login page
    """
    _dump_args(request, "login")
    dacs_user = request.environ.get("DACS_USERNAME", None)
    next_url = request.GET.get("url", None)
    site = request.GET.get("site", None)

    if dacs_user is not None:
        # Already authenticated
        if site:
            if not next_url:
                # We need a url to redirect to, so if we weren't provided one,
                # we pick a reasonable one.
                next_url = reverse("home")

            # Build the absolute url
            next_url = request.build_absolute_uri(next_url)

            # Try to protect against redirect loops.
            # Since we are not able to tell if we get here from
            # dacs_auth_transfer or from someone asking for a login+auth
            # transfer, we risk an infinite redirect loop if we are called with
            # a 'url' argument putting to ourselves with all our GET arguments.
            my_url = request.build_absolute_uri(reverse("sso_login"))
            if next_url.startswith(my_url):
                next_url = request.build_absolute_uri(reverse("home"))

            # Initiate auth transfer
            return make_auth_transfer_response(site, request.environ["DACS_IDENTITY"], next_url)
        elif next_url:
            return redirect(next_url)
        else:
            return redirect(reverse("home"))
    elif site:
        # Not authenticated, and auth transfer is needed after logging in
        query = { "site": site }
        if next_url:
            query["url"] = next_url
        next_url = reverse("sso_login") + "?" + urlencode(query)

    return render(request, "sso/login.html", {
        "dacs_user": dacs_user,
        "next_url": next_url,
        "site": site,
    })

def logout(request):
    """
    Logout page
    """
    _dump_args(request, "logout")
    next_url = request.GET.get("url", None)
    dacs_user = request.environ.get("DACS_USERNAME", None)

    # Can we use JavaScript?
    if request.COOKIES.get(b"nataraja", None):
        # Do not attempt a javascript logout if we are in the middle of a
        # logout redirect dance
        has_javascript = False
    else:
        has_javascript = request.GET.get("javascript", None)
        if has_javascript is None:
            has_javascript = request.COOKIES.get("javascript", None)
        has_javascript = has_javascript == "yes"

    if has_javascript:
        # JS-based logout
        return render(request, "sso/logout.html", {
            "next_url": next_url,
            "federations": [(name, info) for name, info in settings.DEBIAN_FEDERATION.iteritems() if not info.get("skip_logout_dance", None)],
            "logged_in": request.user.is_authenticated,
        })

    if dacs_user is not None:
        # http://en.wikipedia.org/wiki/Nataraja
        #
        # Nataraja is a depiction of the god Shiva as the cosmic dancer who
        # performs his divine dance to destroy a weary universe and make
        # preparations for the god Brahma to start the process of creation.
        #
        # What better name for the list of steps in our dance to destroy all
        # cookies in all our federation domains?
        #
        # I find coding this so... interesting, that I feel the need to add
        # some epic to it.
        #
        # Build a todo list of redirect links we need to visit, with a
        # non-logout link in the end to break the chain
        redirect_dance = []
        for name, info in settings.DEBIAN_FEDERATION.iteritems():
            # Some sites do not have a dacs_signout wrapper and would break the
            # logout dance: skip them. FIXME: logging out from them is
            # impossible until we implement javascript-based logout
            if info.get("skip_logout_dance", False): continue
            redirect_dance.append(info["baseurl"] + "/logout")
        # Sort it to make it easier to test
        redirect_dance.sort()
        if next_url is not None:
            redirect_dance.append(next_url)
        else:
            redirect_dance.append(request.build_absolute_uri(reverse("home")))

        res = redirect("https://sso.debian.org/cgi-bin/dacs/dacs_signout")
        res.set_cookie(b"nataraja", json.dumps(redirect_dance), max_age=60)
        return res
    else:
        # If we are dancing the redirect dance, move to the next step
        try:
            redirect_dance = json.loads(request.COOKIES.get(b"nataraja", "[]"))
        except:
            redirect_dance = []

        if redirect_dance:
            res = redirect(redirect_dance.pop(0))
            if redirect_dance:
                res.set_cookie(b"nataraja", json.dumps(redirect_dance), max_age=60)
            else:
                res.delete_cookie(b"nataraja")
            return res
        else:
            # We finished our dance and the last link did not send us away from
            # the logout url. Weird. Let's deal gracefully with it and send
            # them home, or wherever they wanted to be.
            if next_url:
                return redirect(next_url)
            return redirect("home")
