"""
Django settings for debsso project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from django.conf import global_settings
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#7&j(f5&bze3#m6tt5-v%2fb-$$-0n(u-5x_1_a@1rvgev87i6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    'oauth2_provider',
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'django_dacs',
    'deblayout',
    'debssolayout',
    'sso',
)

OAUTH2_PROVIDER = {
    'SCOPES': {"read": "Reading scope", "write": "Writing scope", "openid": "basic Debian SSO", "email": "your email address", "profile": "your Debian profile information"},
    'OPENID_SCOPE': 'openid',
    'EMAIL_SCOPE': 'email',
    'PROFILE_SCOPE': 'profile',
}


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_dacs.auth.DACSRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # Uncomment to authenticate via REMOTE_USER supplied either by Apache and
    # DACS
    'django_dacs.auth.DACSUserBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'debsso.urls'

WSGI_APPLICATION = 'debsso.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'sso.User'

# Map federation names to site base URLs
DEBIAN_FEDERATION = {
    "CONTRIBUTORS": {
        "baseurl": "https://contributors.debian.org",
    },
    "NM": {
        "baseurl": "https://nm.debian.org",
    },
    "NAGIOS": {
        "baseurl": "https://nagios.debian.org",
        "skip_logout_dance": True,
    },
    "TRACKER": {
        "baseurl": "https://tracker.debian.org",
    },
}

LDAP_MAP = {
    '@debian.org': {
        'LDAP_URI': 'ldaps://db.debian.org',
        'DN': 'ou=users,dc=debian,dc=org',
    },
    '@users.alioth.debian.org': {
        'LDAP_URI': 'ldaps://alioth.debian.org',
        'DN': 'ou=Users,dc=alioth,dc=debian,dc=org',
    },
}

DATABASES = {
    'default': dj_database_url.parse(os.environ.get(
        'DJANGO_DATABASE_URL',
        'sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
    ))
}

LDAP_TIMEOUT = 1

# Try importing local settings from local_settings.py, if we can't, it's just
# fine, use defaults from this file
try:
    from debsso.local_settings import *
except:
    pass
