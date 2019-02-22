import calendar
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from money.models import Payment, Category
from money.views.payments.forms import PaymentForm


class MonthViewMixin(object):
    """Mixin class to filter the queryset by month"""

    def get_context_data(self, **kwargs):
        context = super(MonthViewMixin, self).get_context_data(**kwargs)
        context['months'] = self.get_months_name()
        context['selected_month'] = self.get_selected_month()
        context['current_month'] = self.kwargs.get('month', None)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        month_id = self.kwargs.get('month', None)
        if not month_id:
            return qs.filter(date__month=date.today().month, date__year=date.today().year)
        else:
            return qs.filter(date__month=month_id, date__year=date.today().year)

    def get_months_name(self):
        """
        Get the month names from january to the current month
        """
        months_choices = [calendar.month_name[i] for i in range(1, date.today().month + 1)]
        return months_choices

    def get_selected_month(self):
        _selected_month_id = self.kwargs.get('month', None)
        if _selected_month_id:
            try:
                return calendar.month_name[_selected_month_id]
            except IndexError:
                raise Http404


class CategoryViewMixin(object):
    """Mixin to add category names to context"""
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.values('name')

        if 'category' in self.request.GET or 'subcategory' in self.request.GET:
            context['all_filter'] = self.request.path
            for k in 'category', 'subcategory':
                query = self.request.GET.get(k, None)
                if query:
                    context['query'] = k + "=" + query
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if 'category' in self.request.GET:
            qs = qs.filter(category__name__exact=self.request.GET.get('category'))
        elif 'subcategory' in self.request.GET:
            qs = qs.filter(subcategory__name__exact=self.request.GET.get('subcategory'))
        return qs


class PaymentsIndexView(MonthViewMixin, CategoryViewMixin, LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Payment
    paginate_by = 2
    context_object_name = 'payments'
    template_name = 'money/payment/view_month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Cheltuieli'
        context['columns_labels'] = ['Nume', 'Categorie', 'Subcategorie', 'Data', 'Suma', 'Comentariu']

        # get the whole queryset not just the page qs
        paginator = context['paginator']
        total = self.compute_total(paginator.object_list)['total']
        context['total'] = total if total else "0"

        return context

    def compute_total(self, queryset):
        from django.db.models.aggregates import Sum
        return queryset.aggregate(total=Sum('sum'))


class DeletePaymentView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Payment

    def delete(self, *args, **kwargs):
        redirect_to = self.request.GET.get('next', "/")

        payment_id = self.kwargs.get('payment_id')
        if payment_id:
            payment = Payment.objects.get(id=payment_id)
            payment.delete()
            return JsonResponse({'next': redirect_to,
                                 'status_code': 200})
        else:
            return JsonResponse({'next': redirect_to,
                                 'status_code': 404})


class PaymentView(DetailView):
    model = Payment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('next'):
            context['next_url'] = self.request.GET.get('next', None)
            context['action'] = reverse('money.payment.add') + '?next=' + self.request.GET["next"]
        else:
            context['action'] = reverse('money.payment.add')
        return context

    def get(self, *args, **kwargs):
        form = PaymentForm()
        return render(self.request, 'money/payment/add_payment.html', {'form': form})

    def post(self):
        return redirect('/')
