from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Account(models.Model):
    username = models.CharField(primary_key=True, unique=True, max_length=15)
    name = models.CharField(max_length=1000)
    email = models.CharField(unique=True, max_length=1000)
    date_registration = models.DateField()
    subscription = models.BooleanField()
    type = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Account'
        ordering = ['username']

        def __str__(self):
            return self.username

class SubscribedAccounts(models.Model):
    username = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_subs = models.DateField()
    free_trial = models.BooleanField()







