# coding: utf8
# Debian Layout for Django applications
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
from django import http

def deploy_info(request):
    res = http.HttpResponse(content_type="text/plain")

    # Check if there is some general DACS header, to see if DACS is there
    if "DACS_SITE_CONF" in request.environ:
        print("DACS is enabled", file=res)
    else:
        print("DACS is not enabled", file=res)

    # Check if we are receiving DACS cookies
    has_dacs_cookies = False
    for k, v in request.COOKIES.iteritems():
        if k.startswith("DACS"):
            has_dacs_cookies = True

    if has_dacs_cookies:
        print("DACS cookies are not stripped from the environment", file=res)
    else:
        print("DACS cookies are not in the environment (good)", file=res)

    # Check DACS auth info
    if "DACS_USERNAME" in request.environ:
        print("DACS username: {}".format(request.environ["DACS_USERNAME"]), file=res)
    else:
        print("DACS username not found", file=res)

    return res
