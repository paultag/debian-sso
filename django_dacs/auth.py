import django.contrib.auth.backends
import django.contrib.auth.middleware
from django.conf import settings
from collections import namedtuple

# Name the various bits of information DACS gives us
DACSInfo = namedtuple('DACSInfo', ('unknown0', 'unknown1', "jurisdiction", "username"))

TEST_REMOTE_USER = getattr(settings, "DACS_TEST_USERNAME", None)

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
            username = request.META[self.header]
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
            if request.user.username == self.clean_username(username, request):
                return
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(remote_user=username)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
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
        return info.username
