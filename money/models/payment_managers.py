import datetime

from django.db.models import Manager, QuerySet

from money.models import Category


class PaymentTotalManager(Manager):
    """
    manager to compute the totals
    """

    def get_total_by_categories(self, month: int) -> dict:
        """
        Compute the totals by categories of the month
        :param month:
        :return: dict with totals by categories for all categories
        """

        result = dict()
        categories = Category.objects.all()
        for category in categories:
            result[category.name] = self.compute_category_total(category, month)

        return result

    def get_period_total(self, start_date: datetime.date, end_date: datetime.date) -> int:
        """
        Compute total between two dates
        :param start_date:
        :param end_date:
        :return: grand total of period from from_date to end_date. All the categories are considered.
        """
        payments = super().get_queryset().filter(date__gte=start_date, date__lte=end_date)
        return self.__compute_total(payments)

    def get_total(self, month: int) -> int:
        """
        Compute grand total for a month
        :param month: month
        :return: total of the category
        """
        payments = super().get_queryset().filter(date__month=month)
        return self.__compute_total(payments)

    def compute_category_total(self, category_name: str, month: int):
        """ Compute the total of a category based on the month and category name"""
        payments = super().get_queryset().filter(category__name__exact=category_name,
                                                 date__month=month)
        return self.__compute_total(payments)

    def compute_subcategory_total(self, category_name: str, subcategory_name: str, month: int) -> int:
        """
        Compute the total of a subcategory
        :param category_name: category name
        :param subcategory_name: subcategory name
        :param month: month
        :return: total
        """
        payments = super().get_queryset().filter(category__name__exact=category_name,
                                                 subcategory__name__exact=subcategory_name,
                                                 date__month=month)

        return self.__compute_total(payments)

    @staticmethod
    def __compute_total(payments: QuerySet) -> int:
        from django.db.models.aggregates import Sum
        if payments:
            total = payments.aggregate(total=Sum(sum))
            return total['total']
        return 0
