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
from django.utils.translation import ugettext_lazy as _
from collections import namedtuple

DacsErrorCode = namedtuple("DacsErrorCode", ("code", "tag", "sdesc", "ldesc"))

all_codes = (
    DacsErrorCode(900, "NO_RULE", _("Access denied, no applicable rule"),
                  _("All rules were examined but no rule applies to the service request.")),
    DacsErrorCode(901, "BY_RULE", _("Access denied, forbidden by rule"),
                  _("The closest matching rule does not grant the service request.")),
    DacsErrorCode(902, "NO_AUTH", _("Access denied, user not authenticated"),
                  _("No valid credentials were provided and either a) no rule applies or b) the rule does not grant the service request.")),
    DacsErrorCode(903, "REVOKED", _("Access denied, user access revoked"),
                  _("Credentials were explicitly revoked.")),
    DacsErrorCode(904, "BY_REDIRECT", _("Access denied, redirect"),
                  _("A rule has explicitly redirected the user.")),
    DacsErrorCode(905, "ACK_NEEDED", _("Access denied, acknowledgement needed"),
                  _("One or more notices associated with the request must be acknowledged.")),
    DacsErrorCode(906, "LOW_AUTH", _("Access denied, low authentication level"),
                  _("Although valid credentials were provided, they were obtained by an authentication method not strong enough for the requested resource.")),
    DacsErrorCode(907, "BY_SIMPLE_REDIRECT", _("Access denied, simple redirect"),
                  _("A rule has explicitly redirected the user; do not append DACS query arguments.")),
    DacsErrorCode(908, "CREDENTIALS_LIMIT", _("Access denied, too many credentials were submitted"),
                  _("Too many selected credentials accompanied the request.")),
    DacsErrorCode(909, "INACTIVITY", _("Access denied, inactivity timeout"),
                  _("No authenticated requests were made within a designated time interval.")),
    DacsErrorCode(998, "UNKNOWN", _("Access denied, reason unknown"), None),
)

by_code = dict((x.code, x) for x in all_codes)

def error_for_code(code):
    if code is None: return None
    try:
        code = int(code)
    except ValueError:
        return DacsErrorCode(code, "CODE_NOT_INTEGER", _("Unknown, non-integer error code '{}'").format(code),
                             _("Probably there is a new version of DACS which reports error codes that we do not know about. Please report this to DSA"))

    try:
        return by_code[code]
    except KeyError:
        return DacsErrorCode(code, "CODE_UNKNOWN", _("Unknown error code '{}'").format(code),
                             _("Probably there is a new version of DACS which reports error codes that we do not know about. Please report this to DSA"))
