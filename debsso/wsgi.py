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

import sys
project_root = '/srv/sso.debian.org/debsso'
if project_root not in sys.path:
    sys.path.append(project_root)

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "debsso.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
