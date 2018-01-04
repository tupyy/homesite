# -*- coding: utf-8 -*-
# https://thinkster.io/django-angularjs-tutorial
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# This code is triggered whenever a new user has been created and saved to the database
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

class AccountManager(BaseUserManager):
    def create_user(self,username,password=None,**kwargs):
        if not username:
            raise ValueError('Users must have a valid username.')

        account = self.model(
            username=username
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self,username,password,**kwargs):
        account = self.create_user(username,password,**kwargs)
        account.is_admin = True
        account.save()

        return account

class Account(AbstractBaseUser):
    username = models.CharField(max_length=40,unique=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username
