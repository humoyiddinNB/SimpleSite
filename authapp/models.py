from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
from rest_framework.response import Response


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_active=True, is_staff=False, is_superuser=False, **extra_fields):
        user = self.model(phone=phone, password=password, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        return self.create_user(phone=phone, password=password, is_staff=True, is_superuser=True)


class CustomUser(AbstractBaseUser):
    phone = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=200)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'


    def format(self):
        return ({
            'phone' : self.phone,
            'name' : self.name,
            'is_active' : self.is_active,
            'is_staff' : self.is_staff,
            'is_superuser' : self.is_superuser
        })


class OTP(models.Model):
    phone = models.CharField(max_length=12)
    key = models.CharField(max_length=100)

    is_expire = models.BooleanField(default=False)
    is_conf = models.BooleanField(default=False)
    tried = models.IntegerField(default=0)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if self.tried >= 3:
            self.is_expire = True
        super(OTP, self).save()

