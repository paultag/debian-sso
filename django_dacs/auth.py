import django.contrib.auth.backends
import django.contrib.auth.middleware
from django.conf import settings
from collections import namedtuple
import ldap

# Name the various bits of information DACS gives us
DACSInfo = namedtuple('DACSInfo', ('federation', 'unknown1', "jurisdiction", "username"))

TEST_REMOTE_USER = getattr(settings, "DACS_TEST_USERNAME", None)
LDAP_MAP = getattr(settings, "LDAP_MAP", {})
LDAP_TIMEOUT = getattr(settings, "LDAP_TIMEOUT", 1)

class DACSRemoteUserMiddleware(django.contrib.auth.middleware.RemoteUserMiddleware):
    header = 'REMOTE_USER'

    def process_request(self, request):
        from django.contrib import auth
        from django.core.exceptions import ImproperlyConfigured

        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")

        # Allow to force a DACS user string during testing
        if TEST_REMOTE_USER is not None:
            request.META[self.header] = TEST_REMOTE_USER

        try:
            dacs_user = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then return (leaving
            # request.user set to AnonymousUser by the
            # AuthenticationMiddleware).

            # Actually, make really sure we are logged out!
            # See django bug #17869
            if request.user.is_authenticated():
                auth.logout(request)
            return

        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.email == self.clean_username(dacs_user, request):
                return

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(remote_user=dacs_user)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in. Also update the user data from LDAP.
            import ldap
            uri = dn = user_strip = None
            for ldapbackend in LDAP_MAP:
                if user.email.endswith(ldapbackend):
                    uri = LDAP_MAP[ldapbackend]['LDAP_URI']
                    dn = LDAP_MAP[ldapbackend]['DN']
                    user_strip = ldapbackend
                    break
            if uri:
                c = ldap.initialize(uri)
                u = user.email.replace(user_strip, '')
                try:
                    s = c.search_st(base=dn, scope=ldap.SCOPE_SUBTREE, filterstr='(uid=%s)' % u, timeout=LDAP_TIMEOUT)
                except:
                    s = None
                if s and len(s) == 1:
                    user.first_name = s[0][1]['cn'][0]
                    user.last_name = s[0][1]['sn'][0]
                    user.privider = ldapbackend
                    user.save()
            request.user = user
            auth.login(request, user)

class DACSUserBackend(django.contrib.auth.backends.RemoteUserBackend):
    """
    RemoteUserBackend customised to create User objects from Person
    """
    def split_dacs_user(self, username):
        return DACSInfo(*username.split(":"))


    def clean_username(self, username):
        """
        Map usernames from DACS to usernames in our auth database
        """
        # Take the username out of DACS parts
        info = self.split_dacs_user(username)
        if '@' in info.username:
            return info.username
        else:
            return info.username + "@debian.org"
