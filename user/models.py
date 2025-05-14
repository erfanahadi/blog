from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Bloguser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=254)
    bio = models.CharField(max_length=500, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        managed = False
        db_table = 'bloguser'
