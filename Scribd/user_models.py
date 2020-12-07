from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from ScribdProject import settings


class User(AbstractUser):
    is_provider = models.BooleanField(default=False)
    is_support = models.BooleanField(default=False)
    is_suscribed = models.BooleanField(default=False)

    def get_user_profile(self):
        user_profile = None
        if hasattr(self, 'userprofile'):
            user_profile = self.userprofile
        return user_profile

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

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class userProfile(models.Model):
    SUBS_TYPE = (
        ("Free trial", "Free trial"),
        ("Regular", "Regular"),
        ("Pro", "Pro"),
    )
    _subs_type = dict(SUBS_TYPE)

    portrait = models.ImageField(upload_to="images", default='images/clouds.jpg')
    profile_image = models.ImageField(upload_to="images", default='images/unknown.png')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_profile", on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True, default='')

    # suscription
    subs_type = models.CharField(max_length=15, choices=SUBS_TYPE, default="Free trial", null=True)
    nbooks_by_subs = models.IntegerField(default=10, blank=True, null=True)
    expires = models.DateTimeField(default=datetime.now())
    cancelled = models.BooleanField(default=True)

    # bank data control
    first_upgrade = models.BooleanField(default=True)
    n_uploads = models.IntegerField(default=0, blank=True, null=True)
    n_books_followed = models.IntegerField(default=0, blank=True, null=True)

    # payments
    card_titular = models.CharField(max_length=20, default='', blank=True)
    card_number = models.CharField(max_length=16, default='', blank=True)
    card_expiration = models.CharField(max_length=7, default='', blank=True)
    card_cvv = models.CharField(max_length=3, default='', blank=True)

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)


class providerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="provider_profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    publisher = models.CharField(verbose_name='Provider', max_length=255, blank=True)

    def __str__(self):
        return 'Profile of Provider: {}'.format(self.publisher)

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'


class supportProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="support_profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    user.is_staff = True

    def __str__(self):
        return 'Profile of Support: {}'.format(self.name)

    class Meta:
        verbose_name = 'Support'
        verbose_name_plural = 'Supports'
