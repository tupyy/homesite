from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager
from eventtools.models import BaseEvent, BaseOccurrence


from contract.models import Contract
from money.models.category import Category, Subcategory


class PaymentManager(Manager):
    """
    manager to compute the totals
    """

    def compute_categories(self, month):
        """
        Compute the totals by categories of the month
        :param month:
        :return: dict with totals by categories
        """

        result = dict()
        categories = Category.objects.all()
        for category in categories:
            result[category.name] = self.compute_category_total(category, month)

        return result

    def compute_total(self, from_date, to_date):
        """
        Compute total between two dates
        :param from_date:
        :param to_date:
        :return:
        """
        payments = Payment.objects.filter(date__gte=from_date, date__lte=to_date)
        return self.__compute_total(payments)

    def compute_total2(self, month):
        """
        Compute grand total for a month
        :param month:
        :return:
        """
        payments = Payment.objects.filter(date__month=month)
        return self.__compute_total(payments)

    def compute_category_total(self, category_name, month):
        payments = Payment.objects.filter(category__name__exact=category_name, date__month=month)

        return self.__compute_total(payments)

    def compute_category_total2(self, category_name, subcategory_name, month):
        payments = Payment.objects.filter(category__name__exact=category_name,
                                          subcategory__name__exact=subcategory_name,
                                          date__month=month)

        return self.__compute_total(payments)

    @staticmethod
    def __compute_total(payments):
        total = 0
        for payment in payments:
            total += payment.sum

        return str(total)


class AbstractPayment(models.Model):
    """
    Abstract model for all kind of payments
    """
    contract = models.ForeignKey(Contract, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    subcategory = models.ForeignKey(Subcategory, null=True, on_delete=models.SET_NULL)
    date = models.DateField()
    sum = models.DecimalField(max_digits=8, decimal_places=2)
    comments = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        abstract = True


class Payment(AbstractPayment):
    """
    Model for the a single payment. It can be a payment in a shop
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    nb_tickete = models.IntegerField(default=0, null=True, blank=True)

    objects = models.Manager()
    totals = PaymentManager()

    class Meta:
        ordering = ['-date']
        verbose_name = "payment"
        verbose_name_plural = "payments"

    def __str__(self):
        if self.contract.name:
            return self.contract.name
        return self.category.name + "_" + self.subcategory.name


class RecurrentPayment(AbstractPayment, BaseEvent):
    """
    Model for a recurrent payment
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

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