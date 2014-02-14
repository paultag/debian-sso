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
from django.shortcuts import render, redirect

def _dump_args(request, tag):
    import datetime, os
    now = datetime.datetime.utcnow()
    with open("/tmp/sso-log-" + tag, "at") as fd:
        os.fchmod(fd.fileno(), 0640)
        print("--- {}".format(now.strftime("%Y-%m-%d %H:%M:%S")), file=fd)
        for k, v in request.GET.iteritems():
            print("GET {} -> {}".format(k, v), file=fd)
        for k, v in request.environ.iteritems():
            print("ENV {} -> {}".format(k, v), file=fd)
        for k, v in request.COOKIES.iteritems():
            print("COOKIE {} -> {}".format(k, v), file=fd)

def acs_error(request):
    """
    Access denied / login required page
    """
    from .dacs_codes import error_for_code
    _dump_args(request, "acs_error")
    return render(request, "sso/login.html", {
        "dacs_error": error_for_code(request.GET.get("DACS_ERROR_CODE", None)),
        "dacs_error_url": request.GET.get("DACS_ERROR_URL"),
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

    return render(request, "sso/login.html", {
        "dacs_user": dacs_user,
        "next_url": next_url,
    })

def logout(request):
    """
    Logout page
    """
    _dump_args(request, "logout")
    next_url = request.GET.get("url", None)

    # $c->stash->{message}  = "User logged out.";
    # $c->stash->{hide_loginbox} = 1;

    if next_url:
        res = redirect(next_url)
    else:
        res = render(request, "sso/login.html", {
        })

    #test_cookies = {
    #    "DACS|DEBIANORG||DEBIAN|enrico": "foo",
    #    "DACS|DEBIANORG||DEBIAN|foobar": "foo"
    #}
    #for k, v in test_cookies.iteritems():
    for k, v in request.COOKIES.iteritems():
        if not k.startswith("DACS"): continue
        ## DACS Cookies contain ":" characters, which are not allowed in cookies.
        ## However, our WSGI wrapper converts those to |
        res.delete_cookie(k, domain=".debian.org")

    return res
