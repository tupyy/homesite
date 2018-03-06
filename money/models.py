# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from authentication.models import Account


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
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category,related_name='subcategories',on_delete=models.CASCADE)
    name = models.CharField(max_length=30,null=False)
    description = models.CharField(max_length=30,null=True,blank=True)

    class Meta:
        unique_together = ('name','id')
        ordering = ['id']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return "{} {}".format(self.id,self.name)


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
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    subcategory = models.ForeignKey(Subcategory,null=True,on_delete=models.SET_NULL)
    date = models.DateField()
    sum = models.DecimalField(max_digits=8, decimal_places=2)
    option_pay = models.ForeignKey(PaymentOption,null=True, on_delete=models.SET_NULL)
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
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    subcategory = models.ForeignKey(Subcategory, null=True, on_delete=models.SET_NULL)
    sum = models.DecimalField(max_digits=5, decimal_places=2)
    comments = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user.username



class Total(object):

    def __init__(self,categorie,total,created=None):
        self.categorie = categorie
        self.total = total
        self.total_prev_1 = ""
        self.total_prev_2 = ""


