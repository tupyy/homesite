# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Model for the categories
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,null=False)
    description = models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """
    Model for the subcategories
    """
    category = models.ForeignKey(Category,related_name='subcategories',on_delete=models.CASCADE)
    name = models.CharField(max_length=30,null=False)
    description = models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return self.name


class PaymentOption(models.Model):
    """
    Model for payment options: tickete si check vacance
    """
    name = models.CharField(max_length=15,null=False)

    def __str__(self):
        return self.name


class PaymentModel(models.Model):
    """
    Model for the spending entry
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(Subcategory)
    date = models.DateField()
    sum = models.DecimalField(max_digits=8, decimal_places=2)
    option_pay = models.ForeignKey(PaymentOption)
    nb_option = models.IntegerField(default=0)
    comments = models.CharField(max_length=200,null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.user.username


class PermanentPaymentModel(models.Model):
    """
    Model a permanent payment. It supposed to be payed each month
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(Subcategory)
    sum = models.DecimalField(max_digits=5, decimal_places=2)
    comments = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user.username






