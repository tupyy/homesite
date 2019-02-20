from django.db.models import Manager

from money.models import Category


class PaymentManager(Manager):
    def qet_queryset(self):
        return super().get_queryset().values('user__username',
                                             'category__name',
                                             'subcategory__name',
                                             'date',
                                             'sum',
                                             'comments')


class PaymentTotalManager(Manager):
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
        payments = super().get_queryset().filter(date__gte=from_date, date__lte=to_date)
        return self.__compute_total(payments)

    def compute_total2(self, month):
        """
        Compute grand total for a month
        :param month:
        :return:
        """
        payments = super().get_queryset().filter(date__month=month)
        return self.__compute_total(payments)

    def compute_category_total(self, category_name, month):
        payments = super().get_queryset().filter(category__name__exact=category_name, date__month=month)

        return self.__compute_total(payments)

    def compute_category_total2(self, category_name, subcategory_name, month):
        payments = super().get_queryset().filter(category__name__exact=category_name,
                                          subcategory__name__exact=subcategory_name,
                                          date__month=month)

        return self.__compute_total(payments)

    @staticmethod
    def __compute_total(payments):
        total = 0
        for payment in payments:
            total += payment.sum

        return str(total)