# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import is_safe_url

from money.models import Payment
from .forms import PaymentForm


def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()




@login_required
def update_payments2(request, id=0):
    if request.method == 'GET':
        payment = get_object_or_404(Payment, pk=id)
        form = PaymentForm(instance=payment)
        return render(request, 'money/payment/add_payment.html', {'form': form,
                                                          'next_url': request.GET["next"],
                                                          'action': '/money/payment/update/' + str(id) + '/'})
    elif request.method == 'POST':
        payment = get_object_or_404(Payment, pk=id)
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()

            redirect_to = request.POST.get('next_url')
            url_is_safe = is_safe_url(redirect_to)
            if redirect_to and url_is_safe:
                return HttpResponseRedirect(redirect_to)
            else:
                return redirect("/")

        else:
            form = PaymentForm()
        return render(request, 'money/payment.html', {'form': form})


