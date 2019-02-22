import calendar
from datetime import datetime

from django.views.generic import ListView

from money.models import Payment
from money.utils import get_future_payments


class FuturePaymentsViewMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_payments'] = get_future_payments()
        return context


class TotalPaymentsViewMixin(object):
    model = Payment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_month = datetime.today().month
        last_three_month = self.get_month_range(current_month, 3)

        data = []
        for month in last_three_month:
            month_total = Payment.totals.get_total_by_categories(month)
            month_total = sorted(month_total.items(), key=lambda k: k[0])
            month_total.append(('total', Payment.totals.get_total(month)))
            data.append(month_total)
        context['totals'] = self.transpose(data)
        context['columns_labels'] = ['categorie', *self.get_data_header(last_three_month)]
        return context

    def get_month_range(self, month_index, range_size):
        """
        Return a range of month representing the last range_size month of month_index
        :param month_index month from which we count back range_size month
        :param range_size how many month we go back
        :return list
        """
        month_range = []
        if range_size < 0 and not 0 < month_index < 13:
            return month_range

        for i in range(1, range_size):
            if month_index - i > 0:
                month_range.append(month_index - i)
        month_range.append(month_index)
        return sorted(month_range)

    def get_data_header(self, month_range):
        """ Return the a list with month name based on month_rage"""
        header = []
        for i in month_range:
            if 0 < i < 12:
                header.append(calendar.month_name[i])
        return header

    def transpose(self, data):
        """
        transpose a list of dictionaries like:
        [
            [a: 0, b : 0, c: 0],
            [a: 1, b : 1, c: 1],
        }
        to
        [
            [a, 0, 1],
            [b, 0, 1]
            [c, 0, 1]
        }
        :param data:
        :return: list
        """
        transposed = []
        for item in data[0]:
            transposed.append([item[0], item[1]])
        for item in transposed:
            key = item[0]
            for row in data[1:]:
                for j in row:
                    if j[0] == key:
                        item.append(j[1])
                        break
        return transposed


class IndexView(TotalPaymentsViewMixin, FuturePaymentsViewMixin, ListView):
    model = Payment
    template_name = 'index.html'
