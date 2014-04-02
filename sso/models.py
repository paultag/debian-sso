from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, provider, password=None, **other_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            **other_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields["is_superuser"] = True
        return self.create_user(email, **other_fields)


class User(PermissionsMixin, models.Model):
    objects = UserManager()

    # http://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address
    email = models.CharField(max_length=255, unique=True)
    last_login = models.DateTimeField(_('last login'), default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = True
    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True)
    provider = models.CharField(_('sso auth provider'), max_length=100, blank=True)

    def get_email(self):
        return self.email

    def get_provider(self):
        return self.provider

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def get_username(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        pass

    def check_password(self, raw_password):
        return False

    def set_unusable_password(self):
        pass

    def has_usable_password(self):
        return False

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


