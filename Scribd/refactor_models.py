from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from ScribdProject import settings


class User(AbstractUser):
    is_provider = models.BooleanField(default=False)
    is_support = models.BooleanField(default=False)
    is_suscribed = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to="images", default='images/unknown.png')

    def get_provider_profile(self):
        provider_profile = None
        if hasattr(self, 'providerprofile'):
            provider_profile = self.providerprofile
        return provider_profile

    def get_support_profile(self):
        support_profile = None
        if hasattr(self, 'supportprofile'):
            support_profile = self.supportprofile
        return support_profile

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class userProfile(models.Model):
    SUBS_TYPE = (
        ("Free trial", "Free trial"),
        ("Regular", "Regular"),
        ("Pro", "Pro"),
    )
    _subs_type = dict(SUBS_TYPE)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    bio = models.CharField(max_length=500, blank=True, default='Description not modified')
    nbooks_by_subs = models.IntegerField(default=10, blank=True, null=True)

    # suscription
    subs_type = models.CharField(max_length=15, choices=SUBS_TYPE, blank=True, null=True)
    expires = models.DateTimeField(default=datetime.now() + timedelta(days=7))
    cancelled = models.BooleanField(default=True)

    # payments
    card_titular = models.CharField(max_length=20, default='', blank=True)
    card_number = models.CharField(unique=True, max_length=16, default='', blank=True)
    card_expiration = models.CharField(max_length=7, default='', blank=True)
    card_cvv = models.CharField(max_length=3, default='', blank=True)


class providerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    publisher = models.CharField(verbose_name='Provider', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'


class supportProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    user.is_staff = True

    class Meta:
        verbose_name = 'Support'
        verbose_name_plural = 'Supports'
