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

from django.conf.urls import patterns, url

urlpatterns = patterns('sso.views',
    url(r'^acs_error$', 'acs_error', name="sso_acs_error"),
    url(r'^login_error$', 'login_error', name="sso_login_error"),
    url(r'^login$', 'login', name="sso_login"),
    url(r'^logout$', 'logout', name="sso_logout"),
)

