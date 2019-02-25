from datetime import datetime

from django.db.models import Manager, QuerySet

from money.models import Category


class PaymentTotalManager(Manager):
    """
    manager to compute the totals
    """

    def get_total_by_categories(self, month: int, year=datetime.now().year) -> dict:
        """
        Compute the totals by categories of the month
        :param year: year of the total
        :param month: month of the total
        :return: dict with totals by categories for all categories
        """

        result = dict()
        categories = Category.objects.all()
        for category in categories:
            result[category.name] = self.get_category_total(category, month, year=year)

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
        :return: total of the month for all categories
        """
        payments = self.__get_queryset(month=month,
                                       year=datetime.now().year)
        return self.__compute_total(payments)

    def get_year_total(self, month, year=datetime.now().year) -> int:
        """Compute grand total for a month for a particular year"""
        payments = self.__get_queryset(month=month,
                                       year=year)
        return self.__compute_total(payments)

    def get_category_total(self, category_name: str, month: int, year=datetime.now().year):
        """ Compute the total of a category based on the month and category name for the current year"""
        payments = self.__get_queryset_by_category(category_name, month, year=year)
        return self.__compute_total(payments)

    def get_subcategory_total(self, category_name: str, subcategory_name: str, month: int, year=datetime.now().year) -> int:
        """
        Compute the total of a subcategory
        :param category_name: category name
        :param subcategory_name: subcategory name
        :param month: month
        :param year: year of the total
        :return: total
        """
        payments = super().get_queryset().filter(category__name__exact=category_name,
                                                 subcategory__name__exact=subcategory_name,
                                                 date__month=month,
                                                 date__year=year)

        return self.__compute_total(payments)

    def __get_queryset_by_category(self, category, month, year=datetime.now().year):
        return super().get_queryset().filter(category__name=category,
                                             date__month=month,
                                             date__year=year)

    def __get_queryset(self, month, year):
        return super().get_queryset().filter(date__month=month,
                                             date__year=year)

    @staticmethod
    def __compute_total(payments: QuerySet) -> int:
        from django.db.models.aggregates import Sum
        if payments:
            total = payments.aggregate(total=Sum('sum'))
            return total['total']
        return 0
