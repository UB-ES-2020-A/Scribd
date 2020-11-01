from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name,type, password=None):
        # crea un usuari
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),
                          username=username,
                          first_name=first_name,
                          last_name=last_name,
                          type = type)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password=None):
        user = self.create_user(email="admin@gmail.com",
                                username=username,
                                first_name=first_name,
                                last_name=last_name,
                                password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    username = models.CharField(primary_key=True, unique=True, max_length=20)
    first_name = models.CharField(max_length=100,blank=False,default='')
    last_name = models.CharField(max_length=100,blank=False, default='')
    # no posem password perque esta ja fet a la mateixa classe
    date_registration = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_subscribed = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USER_TYPE = (
        ("admin", "admin"),
        ("provider", "provider"),
        ("support", "support"),
        ("free_trial", "free_trial"),
        ("subscribed", "subscribed"),
    )
    _type_user = dict(USER_TYPE)
    type = models.CharField(max_length=15, choices=USER_TYPE, default="subscribed")

    USERNAME_FIELD = 'username'  # el que identificara a la classe
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.username

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


class SubscribedUsers(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    date_subs = models.DateField(auto_now_add=True)
    free_trial = models.BooleanField()