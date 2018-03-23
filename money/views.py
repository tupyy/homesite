# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

import utils
from money.forms import PaymentForm
from money.serialize import *

"""
    Djano classic view
"""


def index(request):
    months_choices = []
    for i in range(1, date.today().month + 1):
        months_choices.append(calendar.month_name[i])

    next_payments = utils.get_future_payments()

    return render(request, 'index.html', {'luni': months_choices,
                                          'next_payments': next_payments})


def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()

    form = PaymentForm()
    return render(request, 'money/add_payment.html', {'form': form,
                                                      'next_url': request.GET["next"],
                                                      'action': '/money/payment/?next=' + request.GET["next"]})


@login_required
def update_payments2(request, id=0):
    if request.method == 'GET':
        payment = get_object_or_404(Payment, pk=id)
        form = PaymentForm(instance=payment)
        return render(request, 'money/add_payment.html', {'form': form,
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


@login_required
def delete_payment(request, id=0):
    """
    Delete a payment
    :param request:
    :param pk: PrimaryKey
    :return:
    """

    if request.method == 'POST':
        payment = get_object_or_404(Payment, pk=id)
        payment.delete()

        redirect_to = request.POST.get('next_url')
        url_is_safe = is_safe_url(redirect_to)
        if redirect_to and url_is_safe:
            return HttpResponseRedirect(redirect_to)
        else:
            return redirect("/")
    else:
        return HttpResponseNotAllowed('GET')


@login_required
def view_payments(request, month=13):
    categories = Category.objects.all()

    months_choices = []
    for i in range(1, date.today().month + 1):
        months_choices.append(my_calendar.month_name[i])

    # Get payments for the current month
    if month > 12:
        payments = Payment.objects.filter(date__month=date.today().month, date__year=date.today().year)
        selected_month = date.today().month
    else:
        payments = Payment.objects.filter(date__month=month, date__year=date.today().year)
        selected_month = month

    if len(payments) > 0:
        return render(request, 'money/view_month.html', {
            'categorii': categories,
            'luni': months_choices,
            'selected_month': selected_month,
            'payments': payments
        })
    else:
        return render(request, 'money/view_month.html', {
            'categorii': categories,
            'luni': months_choices,
            'selected_month': selected_month,
            'payments': payments,
            'error_message': 'Nothing to show'
        })


@login_required
def update_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    form = PaymentForm(instance=payment)

    return render("money/add_payment.html", {'form': form})
