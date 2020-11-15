from datetime import datetime

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from ScribdProject import settings
from django.contrib import auth
from datetime import date
from django.utils.translation import ugettext as _, ungettext, ugettext_lazy

import Scribd.models


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name,subs_type = "Free Trial", password=None):
        # crea un usuari
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),
                          username=username,
                          first_name=first_name,
                          last_name=last_name,
                          subs_type=subs_type
                          )

        user.set_password(password)
        user.user_type = "User"

        if user.subs_type == "Free Trial":
            user.nbooks_by_subs = 10
        if user.subs_type == "Regular":
            user.nbooks_by_subs = 100
        if user.subs_type == "Pro":
            user.nbooks_by_subs = 1000

        user.save(using=self._db)
        """if user_type == "Provider":
            self.create_provider(user)"""
        return user

    """def create_provider(self, user):
        provider = Provider(username=user.username)
        provider.save(using=self._db)
        return provider"""


    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(email=email,
                                username=username,
                                first_name=first_name,
                                last_name=last_name,
                                password=password)

        user.is_admin = True
        user.user_type = "Admin"
        user.subs_type = "Pro"
        user.save(using=self._db)
        return user



class SubscribedUsers(models.Model):
    SUBS_TYPE = (
        ("Free trial", "Free trial"),
        ("Regular", "Regular"),
        ("Pro", "Pro"),
    )
    _subs_type = dict(SUBS_TYPE)

    #username = models.ForeignKey('User', on_delete=models.CASCADE,null=True, blank=True)
    #username = models.OneToOneField('User', on_delete=models.CASCADE, blank=True, null=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_subs = models.DateField(auto_now_add=True,null=True, blank=True)
    card_titular = models.CharField(max_length=20, default='', blank=True)
    card_number = models.CharField(unique=True, max_length=16, default='',blank=True)
    card_expiration = models.CharField(max_length=7, default='',blank=True)
    card_cvv = models.CharField(max_length=3, default='',blank=True)

    price = models.DecimalField(max_digits=64, decimal_places=2)
    trial_period = models.PositiveIntegerField(null=True, blank=True)
    trial_unit = models.CharField(max_length=1, null=True, choices=_subs_type)
    recurrence_period = models.PositiveIntegerField(null=True, blank=True)
    recurrence_unit = models.CharField(max_length=1, null=True,
                                       choices=_subs_type)
    group = models.ForeignKey(auth.models.Group, null=False, blank=False, unique=False, on_delete=models.PROTECT)



    class Meta:
        verbose_name = 'SubscribedUser'
        verbose_name_plural = 'SubscribedUsers'

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ("Admin", "Admin"),
        ("Provider", "Provider"),
        ("Support", "Support"),
        ("User", "User"),
    )
    _type_user = dict(USER_TYPE)

    SUBS_TYPE = (
        ("Free trial", "Free trial"),
        ("Regular", "Regular"),
        ("Pro", "Pro"),
    )
    _subs_type = dict(SUBS_TYPE)


    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(primary_key=True, unique=True, max_length=20)
    first_name = models.CharField(max_length=100, blank=False, default='')
    last_name = models.CharField(max_length=100, blank=False, default='')
    # no posem password perque esta ja fet a la mateixa classe
    date_registration = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # profile attributes
    profile_image = models.ImageField(upload_to="images", default='images/unknown.png')
    about_me = models.CharField(max_length=500, blank=True, default='Description not modified')
    nbooks_by_subs = models.IntegerField(default=10)
    group = models.ForeignKey(auth.models.Group, null=False, blank=False, unique=False, on_delete=models.PROTECT)


    user_type = models.CharField(max_length=15, choices=USER_TYPE, default="User")
    subs_type = models.CharField(max_length=15, choices=SUBS_TYPE, default="Free trial")
    #subs_type = models.ForeignKey(SubscribedUsers, verbose_name='subs_type', on_delete=models.CASCADE, null=True)


    expires = models.DateField(null=True, default=date.today)
    active = models.BooleanField(default=True)
    cancelled = models.BooleanField(default=True)

    objects = models.Manager()

    USERNAME_FIELD = 'username'  # el que identificara a la classe
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = UserManager()

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.username

    def get_email_field_name(self):
        return self.email

    def get_user_type(self):
        return self._type_user[self.type]

    def _str_(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # si te algun permis
        return True

    def has_module_perms(self, app_label):
        # te permisos per veure app_label
        return True

    def is_staff(self):
        # si es admin si
        return self.is_admin

    @property
    def is_active(self):
        return True
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'



class Provider(models.Model):
    username = models.OneToOneField('User', on_delete=models.CASCADE, blank=True, null=True)
    publisher = models.CharField(verbose_name='Publisher', max_length=255,blank=True)
    group = models.ForeignKey(auth.models.Group, null=False, blank=False, unique=False, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'

