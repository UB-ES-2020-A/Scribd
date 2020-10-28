from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.
from django.urls import reverse

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm



class User(models.Model):

    USER_TYPE = (
        ("admin","admin"),
        ("provider","provider"),
        ("support","support"),
        ("free_trial","free_trial"),
        ("subscribed","subscribed"),
    )
    _type_user = dict(USER_TYPE)

    username = models.CharField(primary_key=True, unique=True, max_length=20)
    name = models.CharField(max_length=1000)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    date_registration = models.DateField(auto_now_add=True)
    subscription = models.BooleanField()
    type = models.CharField(max_length=15, choices=USER_TYPE)

    def get_user_type(self):
        return self._type_user[self.type]

    class Meta:
        verbose_name = 'User'
        ordering = ['username']

        def __str__(self):
            return self.username


class SubscribedUsers(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    date_subs = models.DateField(auto_now_add=True)
    free_trial = models.BooleanField()


class Ebook(models.Model):
    TYPE_FILE = (
        ("pdf", "pdf"),
        ("epub", "epub"),
    )
    _type_files = dict(TYPE_FILE)
    
    ebook_number = models.CharField(max_length=8, unique=True, default='') #IBAN?
    title = models.CharField(max_length=50, blank=False, default='')
    autor = models.CharField(max_length=50, blank=False, default='')
    description = models.TextField(default='')
    is_promot = models.BooleanField(default='False')
    size = models.IntegerField(default=0)
    media_type = models.CharField(max_length=5, choices=TYPE_FILE, default='')
    featured_photo = models.ImageField(upload_to="scribd/static/images/",default='scribd/static/images/')
    count_downloads = models.PositiveIntegerField(default=0)

    def get_ebook_media_type(self):
        return self._type_files[self.media_type]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ebook'
        verbose_name_plural = 'Ebooks'


class ViewedEbooks(models.Model):
    id_vr = models.AutoField(primary_key=True)
    ebook = models.ManyToManyField(Ebook, through='EbookInsertDate')


class EbookInsertDate(models.Model):
    viewed_ebooks = models.ForeignKey(ViewedEbooks, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']


class Review(models.Model):
    STARS = (
        ("One star", 1),
        ("Two stars", 2),
        ("Three stars", 3),
        ("Four stars", 4),
        ("Five stars", 5),
    )
    _d_stars = dict(STARS)
    id = models.AutoField(primary_key=True)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    value_stars = models.CharField(max_length=12, choices=STARS)
    comment = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def get_human_stars(self):
        return self._d_stars[self.value_stars]

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

