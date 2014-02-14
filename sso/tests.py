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
