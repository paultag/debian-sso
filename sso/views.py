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

from django.shortcuts import render

def acs_error(request):
    return render(request, "sso/ACS_ERROR_HANDLER.html", {
#        $c->stash->{DACS_ERROR_URL} = $tf->filter($c->req->param('DACS_ERROR_URL'))
#          if ( $c->req->param('DACS_ERROR_URL') );
#        $c->stash->{DACS_ERROR_CODE} = $c->req->param('DACS_ERROR_CODE')
#          if ( $c->req->param('DACS_ERROR_CODE') );
    })

def login_error(request):
#        if ( $c->req->param('DACS_ERROR_URL') ) {
#                $c->stash->{DACS_ERROR_URL} = $tf->filter($c->req->param('DACS_ERROR_URL'));
#        }
    return render(request, "sso/login_error.html", {
    })

def login(request):
#        if ( $ENV{DACS_USERNAME} ) {
#                $c->stash->{title}      = "Login: Logged in as $ENV{DACS_USERNAME}";
#        } else {
#                $c->stash->{title}    = "Login";
#                $c->stash->{hide_loginbox} = 1;
#        }
    return render(request, "sso/login.html", {
    })

def logout(request):
#        foreach my $cookie ( keys %{ $c->request->cookies } ) {
#                if ( $cookie =~ /^DACS/ ) {
#                        ## DACS Cookies contain ":" characters, which are not allowed in cookies.
#                        ## CGI::Cookie encodes the ":" resulting in cookies not beind properly
#                        ## expired. So we have to expire the cookie ourselves by directly manipulating
#                        ## the response header.
#                        my $cgi_cookie = $c->request->cookies->{$cookie};
#                        my $domain     = $c->request->uri->host;
#                        $domain =~ s/.*(\.[a-z,0-9,-]+\.[a-z,0-9,-]+)$/$1/;
#                        $c->res->headers->push_header(
#                                                               'Set-Cookie' => $cgi_cookie->name . "="
#                                                                 . $cgi_cookie->value
#                                                                 . "; path=/; domain="
#                                                                 . $domain
#                                                                 . ";  expires=Thu, 01-Jan-1970 00:00:01 GMT" );
#                }
#        }
#
#        $c->stash->{message}  = "User logged out.";
#        $c->stash->{hide_loginbox} = 1;
#}
    return render(request, "sso/login.html", {
    })
