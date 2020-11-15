from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name,subs_type= "Free Trial", password=None):
        # crea un usuari
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),
                          username=username,
                          first_name=first_name,
                          last_name=last_name,
                          subs_type=subs_type,
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
        return user

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


class User(AbstractBaseUser, PermissionsMixin):
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
    profile_image = models.ImageField(upload_to="static/images/", default='/static/images/unknown.png')
    about_me = models.CharField(max_length=500, blank=True, default='Description not modified')
    nbooks_by_subs = models.IntegerField(default=10)

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

    user_type = models.CharField(max_length=15, choices=USER_TYPE, default="User")
    subs_type = models.CharField(max_length=15, choices=SUBS_TYPE, default="Free trial")

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


class SubscribedUsers(models.Model):

    username = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    #type = models.OneToOneField('User', on_delete=models.CASCADE, blank=True, null=True)
    date_subs = models.DateField(auto_now_add=True,null=True, blank=True)
    card_titular = models.CharField(max_length=20, default='', blank=True)
    card_number = models.CharField(unique=True, max_length=16, default='',blank=True)
    card_expiration = models.CharField(max_length=7, default='',blank=True)
    card_cvv = models.CharField(max_length=3, default='',blank=True)
