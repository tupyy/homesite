from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager
from django.db.models import Model
from eventtools.models import BaseEvent, BaseOccurrence

from contract.models import Contract
from money.models.category import Category, Subcategory
from money.models.payment_managers import PaymentManager


class Payment(Model):
    """
    Model for the a single payment. It can be a payment in a shop
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    subcategory = models.ForeignKey(Subcategory, null=True, on_delete=models.SET_NULL)
    date = models.DateField()
    sum = models.DecimalField(max_digits=8, decimal_places=2)
    comments = models.CharField(max_length=200, null=True, blank=True)

    objects = PaymentManager()
    totals = PaymentTotalManager()

    class Meta:
        ordering = ['-date']
        verbose_name = "payment"
        verbose_name_plural = "payments"

    def __str__(self):
        return self.category.name + "_" + self.subcategory.name


class RecurrentPayment(Payment, BaseEvent):
    """
    Model for a recurrent payment
    """
    contract = models.ForeignKey(Contract, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.contract.name:
            return self.contract.name
        else:
            return self.id


class PaymentOccurrence(BaseOccurrence):
    payment = models.ForeignKey(RecurrentPayment, on_delete=models.CASCADE)

    def __str__(self):
        if self.payment.contract.name:
            return self.payment.contract.name
        else:
            return self.payment.id


class Total(object):
    def __index__(self, categorie, total, total_prev1, total_prev2):
        self.categorie = categorie
        self.total = total
