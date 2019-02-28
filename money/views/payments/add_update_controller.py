from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from money.models import Payment
from money.views.payments.forms import PaymentForm


class PaymentFormViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_url'] = self.request.GET.get("next", reverse('money.payment.add'))
        return context


class AddPaymentView(PaymentFormViewMixin, TemplateView):
    model = Payment
    template_name = 'money/payment/add_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['action'] = reverse('money.payment.add')
        context['form'] = PaymentForm()
        return context

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(form.cleaned_data['next_url'])
        else:
            return render(self.request, reverse('money.payment.add'), {'form': form,
                                                                       'action': reverse('money.payment.add'),
                                                                       'next_url': reverse('index')})


class UpdatePaymentView(PaymentFormViewMixin, DetailView):
    model = Payment
    template_name = 'money/payment/add_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _payment = self.get_object()
        context['form'] = PaymentForm(instance=_payment)
        context['action'] = reverse('money.payment.update', args=[_payment.id])
        return context

    def post(self, request, pk):
        form = PaymentForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(form.cleaned_data['next_url'])
        else:
            return render(self.request, reverse('money.payment.update', args=[pk]), {'form': form})
