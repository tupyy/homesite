import calendar
from datetime import date

from django.views.generic import ListView

from money.models import Payment, Category


class MonthViewMixin(object):
    """Mixin class to get month names from jan to today"""

    def get_context_data(self, **kwargs):
        context = super(MonthViewMixin, self).get_context_data(**kwargs)
        context['months'] = self.get_months_name()
        context['selected_month'] = self.get_selected_month()
        context['current_month'] = self.kwargs.get('month', None)
        return context

    def get_months_name(self):
        """
        Get the month names from january to the current month
        """
        months_choices = [calendar.month_name[i] for i in range(1, date.today().month + 1)]
        return months_choices

    def get_selected_month(self):
        _selected_month_id = self.kwargs.get('month', None)
        if _selected_month_id:
            return calendar.month_name[_selected_month_id]


class CategoryViewMixin(object):
    """Mixin to add category names to context"""
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.values('name')
        return context


class PaymentView(MonthViewMixin, CategoryViewMixin, ListView):
    model = Payment
    paginate_by = 10
    context_object_name = 'payments'
    template_name = 'money/payment/view_month.html'

    def get_queryset(self):
        qs = super().get_queryset()
        month_id = self.kwargs.get('month', None)
        if not month_id:
            return qs.filter(date__month=date.today().month, date__year=date.today().year)
        else:
            return qs.filter(date__month=month_id, date__year=date.today().year)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Cheltuieli'
        context['columns_labels'] = ['Nume', 'Categorie', 'Subcategorie', 'Data', 'Suma', 'Comentariu']
        return context
