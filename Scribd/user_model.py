from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User
import models


class Subscription(models.Model):
    SUBS_TYPE = (
        ("Free trial", "Free trial"),
        ("Regular", "Regular"),
        ("Pro", "Pro"),
    )
    _subs_type = dict(SUBS_TYPE)

    username = models.CharField(max_length=100, unique=True, null=False)
    date_subs = models.DateField(auto_now_add=True, null=True, blank=True)
    subs_type = models.CharField(max_length=15, choices=SUBS_TYPE, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=64, decimal_places=2, default='0')
    trial_period = models.PositiveIntegerField(null=True, blank=True)
    recurrence_period = models.PositiveIntegerField(null=True, blank=True)
    #group = models.ForeignKey(Group,null=True, blank=False, unique=False, on_delete=models.CASCADE, default=1)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to="images", default='images/unknown.png')
    about_me = models.CharField(max_length=500, blank=True, default='Description not modified')
    nbooks_by_subs = models.IntegerField(default=10, blank=True, null=True)
    subs_type = models.OneToOneField(Subscription, verbose_name='subs_type', on_delete=models.CASCADE, null=True)

    support = models.BooleanField(verbose_name='Support', default=False, null=True, blank=True)
    provider = models.BooleanField(verbose_name='Provider', null=True, blank=True)

    subscription = models.ForeignKey(Subscription, related_name="Subscription",on_delete=models.CASCADE)
    expires = models.DateTimeField(default=datetime.now() + timedelta(days=7))
    active = models.BooleanField(default=True)
    cancelled = models.BooleanField(default=True)

    card_titular = models.CharField(max_length=20, default='', blank=True)
    card_number = models.CharField(unique=True, max_length=16, default='', blank=True)
    card_expiration = models.CharField(max_length=7, default='', blank=True)
    card_cvv = models.CharField(max_length=3, default='', blank=True)


    @property
    def is_support(self):
        return self.support

    @property
    def is_provider(self):
        return self.provider

class Provider(models.Model):
    user = models.OneToOneField(User, related_name="Provider", on_delete=models.CASCADE)
    publisher = models.CharField(verbose_name='Provider', max_length=255, blank=True)
    #group = models.ForeignKey(Group,null=True, blank=False, unique=False, on_delete=models.CASCADE, default=1)
    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'

class Support(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.is_staff= True
    class Meta:
        verbose_name = 'Support'
        verbose_name_plural = 'Supports'