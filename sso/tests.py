from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class SSOTestCase(TestCase):
    def test_login(self):
        # When not authenticated, we get the login form
        c = Client()
        response = c.get(reverse('sso_login'))
        self.assertEquals(response.status_code, 200)
        self.assertIsNone(response.context["dacs_user"])
        self.assert_('<form name="loginForm"' in response.content)
        self.assert_('<h1>Access denied.</h1>' not in response.content)

        # When authenticated, we get a logout button
        response = c.get(reverse('sso_login'), DACS_USERNAME="logged-in-name")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["dacs_user"], "logged-in-name")
        self.assert_('logged-in-name' in response.content)
        self.assert_('<h1>Access denied.</h1>' not in response.content)

        # When authenticated and we have a next url, we redirect
        response = c.get(reverse('sso_login'), data={"url": "http://www.example.org"},
                         DACS_USERNAME="logged-in-name")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "http://www.example.org")

    def test_login_transfer(self):
        # The login form with auth transfer has a next url that points to us
        c = Client()
        response = c.get(reverse('sso_login'), data={"site": "CONTRIBUTORS"})
        self.assertEquals(response.status_code, 200)
        self.assertIsNone(response.context["dacs_user"])
        self.assertEquals(response.context["next_url"], "/sso/login?site=CONTRIBUTORS")
        self.assert_('<form name="loginForm"' in response.content)
        self.assert_('<h1>Access denied.</h1>' not in response.content)

        # The login form with auth transfer has a next url that points to us,
        # then to the original next url
        c = Client()
        response = c.get(reverse('sso_login'), data={"site": "CONTRIBUTORS", "url": "http://www.example.org"})
        self.assertEquals(response.status_code, 200)
        self.assertIsNone(response.context["dacs_user"])
        self.assertEquals(response.context["next_url"], "/sso/login?url=http%3A%2F%2Fwww.example.org&site=CONTRIBUTORS")
        self.assert_('<form name="loginForm"' in response.content)
        self.assert_('<h1>Access denied.</h1>' not in response.content)

        # The login form with auth transfer, when already logged in, initiates
        # auth transfer
        c = Client()
        response = c.get(reverse('sso_login'), data={"site": "CONTRIBUTORS", "url": "http://www.example.org"}, DACS_USERNAME="foo")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "https://sso.debian.org/cgi-bin/dacs/dacs_auth_transfer?DACS_IDENTITY=foo&OPERATION=EXPORT&TARGET_FEDERATION=CONTRIBUTORS&TRANSFER_SUCCESS_URL=http%3A%2F%2Fwww.example.org")

        # If there is no 'url' argument, it picks a sensible
        # TRANSFER_SUCCESS_URL
        c = Client()
        response = c.get(reverse('sso_login'), data={"site": "CONTRIBUTORS"}, DACS_USERNAME="foo")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "https://sso.debian.org/cgi-bin/dacs/dacs_auth_transfer?DACS_IDENTITY=foo&OPERATION=EXPORT&TARGET_FEDERATION=CONTRIBUTORS&TRANSFER_SUCCESS_URL=http%3A%2F%2Ftestserver%2F")

        # If there is a 'url' argument pointing to ourselves, we redirect to
        # home instead to prevent a redirect loop
        c = Client()
        response = c.get(reverse('sso_login'), data={"site": "CONTRIBUTORS", "url": "http://testserver/sso/login"}, DACS_USERNAME="foo")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "https://sso.debian.org/cgi-bin/dacs/dacs_auth_transfer?DACS_IDENTITY=foo&OPERATION=EXPORT&TARGET_FEDERATION=CONTRIBUTORS&TRANSFER_SUCCESS_URL=http%3A%2F%2Ftestserver%2F")

    def test_acs_error(self):
        # When not authenticated, we get the login form
        c = Client()
        response = c.get(reverse('sso_acs_error'), data={"DACS_ERROR_CODE": "902"})
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.context["dacs_error"])
        self.assertIsNone(response.context["dacs_error_url"])
        self.assert_('<h1>Login required</h1>' in response.content)
        self.assert_('<form name="loginForm"' in response.content)
        self.assert_('For access to' not in response.content)

        response = c.get(reverse('sso_acs_error'), data={
            "DACS_ERROR_CODE": "902", "DACS_ERROR_URL": "http://www.example.org"})
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.context["dacs_error"])
        self.assertEquals(response.context["dacs_error_url"], "http://www.example.org")
        self.assert_('<h1>Login required</h1>' in response.content)
        self.assert_('For access to <tt>http://www.example.org' in response.content)
        self.assert_('<form name="loginForm"' in response.content)

        response = c.get(reverse('sso_acs_error'), data={"DACS_ERROR_CODE": "903"})
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.context["dacs_error"])
        self.assertIsNone(response.context["dacs_error_url"])
        self.assert_('<h1>Access denied, user access revoked</h1>' in response.content)
        self.assert_('<form name="loginForm"' in response.content)
        self.assert_('For access to' not in response.content)

    def test_logout_nourl(self):
        # Plain logout, no next_url
        c = Client()
        response = c.get(reverse("sso_logout"), DACS_USERNAME="foo")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "https://sso.debian.org/cgi-bin/dacs/dacs_signout")
        self.assertNotIn("debsso_logout_next_url", c.cookies)

        # Back from logout, redirect to home
        response = c.get(reverse("sso_logout"))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "http://testserver/")
        self.assertNotIn("debsso_logout_next_url", c.cookies)

    def test_logout_url(self):
        # Plain logout, next_url
        c = Client()
        response = c.get(reverse("sso_logout"), data={"url": "http://www.example.org"}, DACS_USERNAME="foo")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "https://sso.debian.org/cgi-bin/dacs/dacs_signout")
        self.assertIn("debsso_logout_next_url", c.cookies)

        # Back from logout, redirect to example.org and clean next_url session
        response = c.get(reverse("sso_logout"))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "http://www.example.org")
        self.assertIn("debsso_logout_next_url", c.cookies)
        self.assertEquals(c.cookies["debsso_logout_next_url"]["expires"], "Thu, 01-Jan-1970 00:00:00 GMT")
