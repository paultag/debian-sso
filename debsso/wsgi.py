# coding: utf8

"""
WSGI config for debsso project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "debsso.settings")

from django.core.wsgi import get_wsgi_application
base_application = get_wsgi_application()

# Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn.
#
# Application wrapper that defangs DACS cookie names, replacing : with | before
# passing control to Django, and replacing | with : in Django's headers
#
# DACS download page (https://dacs.dss.ca/download.html) currently says:
#   This and previous releases of DACS produce HTTP cookies that have colons
#   (and possibly other punctuation) in their names. Although this is not known
#   to cause problems with any web browsers, it is unacceptable to some
#   versions of Tomcat. It seems that RFC 2109 (Sections 4.2.2 and 4.1) and RFC
#   2965 (Sections 3.2.2 and 3.1), with RFC 2616 (Section 2.2), do not allow
#   these "separators" to appear in a cookie name. DACS does not currently have
#   a workaround for this problem, but then it does not claim to be RFC
#   2109/2965 compliant. A future release of DACS will likely change the syntax
#   of its cookies to something benign. Changes to the cookie name syntax may
#   cause problems for interoperation between different versions of DACS. Note
#   that middleware should not be relying upon (esp. parsing) the names of DACS
#   cookies, other than to identify the different types of cookies, so a change
#   should only be a minor inconvenience for middleware.
# A fix can never come too soon: this break of interoperability is giving me
# a terribly frustrating experience.
import re
def application(environ, start_response):
    # Replace : with | in DACS cookies
    re_cleancookies = re.compile(r"\bDACS:[^=]+")
    re_uncleancookies = re.compile(r"^DACS|[^=]+")
    c = environ.get(b"HTTP_COOKIE", None)
    if c is not None:
        environ[b"HTTP_COOKIE"] = re_cleancookies.sub(lambda x:x.group().replace(":", "|"), c)

    def my_start_response(status, headers):
        # Replace | with : in DACS cookie names
        for idx in xrange(len(headers)):
            if headers[idx][0] == b"Set-Cookie":
                headers[idx] = (b"Set-Cookie",
                                re_uncleancookies.sub(
                                    lambda x:x.group().replace(b"|", b":"),
                                    headers[idx][1],
                                    1))
        start_response(status, headers)

    return base_application(environ, my_start_response)
