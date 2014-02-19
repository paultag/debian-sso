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

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='debsso/index.html'), name="home"),

    url(r'^_deploy_info_$', 'deblayout.views.deploy_info'),

    url(r'^sso/', include('sso.urls')),

    url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^license/$', TemplateView.as_view(template_name='license.html'), name="root_license"),
)
