# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
import calendar
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from money.forms import PaymentForm,PermanentPaymentForm
from money.models import PaymentModel, Category, PermanentPaymentModel
from money.serialize import *
from money.tables import MonthTable, TotalTable,ViewPermanentPaymentTable
from money.utils import compute_total, append_to_total

"""
    Djano classic view
"""

def index(request):

    months_choices = []
    for i in range(1, date.today().month + 1):
        months_choices.append(calendar.month_name[i])

    return render(request, 'index.html', {'luni' : months_choices})


def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()

    form = PaymentForm()
    return render(request,'money/add_payment.html',{'form':form,
                                                    'next_url':request.path})

@login_required
def update_payments(request, id=0):

    if request.method == 'GET':
        payment = get_object_or_404(PaymentModel,pk=id)
        form = PaymentForm(instance=payment)
        return render(request,'money/add_payment.html',{'form':form,
                                                        'next_url': request.path})
    elif request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()

            redirect_to = request.POST.get('next')
            url_is_safe = is_safe_url(redirect_to)
            if redirect_to and url_is_safe:
                return HttpResponseRedirect(redirect_to)
            else:
                return redirect("/")

        else:
            form = PermanentPaymentForm()
        return render(request, 'money/payment.html', {'form': form})


def permanent_payment(request):
    if request.method == 'POST':
        form = PermanentPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            if 'submit' in request.POST:
                form = PermanentPaymentForm()
            else:
                return HttpResponseRedirect('/')
    else:
        form = PermanentPaymentForm()
    return render(request,'money/payment.html',{'form': form})


@login_required
def delete_payment(request,id=0):
    """
    Delete a payment
    :param request:
    :param pk: PrimaryKey
    :return:
    """

    if request.method == 'POST':
        payment = get_object_or_404(PaymentModel,pk=id)
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
def delete_permanent_payment(request,id=0):
    """
    Delete a permanent payment
    :param request:
    :param pk:
    :return:
    """
    payment=get_object_or_404(PermanentPaymentModel,pk=id)
    payment.delete()
    return HttpResponseRedirect(request.path)

@login_required
def view_payments(request, month=13):
    categories = Category.objects.all()

    months_choices = []
    for i in range(1, date.today().month + 1):
        months_choices.append(calendar.month_name[i])

    # Get payments for the current month
    if month > 12:
        payments = PaymentModel.objects.filter(date__month=date.today().month, date__year=date.today().year)
        selected_month = date.today().month
    else:
        payments = PaymentModel.objects.filter(date__month=month, date__year=date.today().year)
        selected_month=month

    if len(payments) > 0:
        return render(request,'money/view_month.html',{
                                                        'categorii':categories,
                                                       'luni':months_choices,
                                                        'selected_month':selected_month,
                                                        'payments' : payments
                                                      })
    else:
        return render(request, 'money/view_month.html', {
                                                        'categorii': categories,
                                                        'luni': months_choices,
                                                        'selected_month': selected_month,
                                                        'payments': payments,
                                                        'error_message' : 'Nothing to show'
                                                    })

@login_required
def view_permanent_payments(request):
    table = ViewPermanentPaymentTable(PermanentPaymentModel.objects.all())
    return render(request,'money/month_payments.html' ,{'month_table':table,
                                                        'nav_bar_title':'Viramente periodice lunare'
                                                        })


@login_required
def update_payment(request,payment_id):
    payment = get_object_or_404(PaymentModel,pk=payment_id)
    form = PaymentForm(instance=payment)

    return render("money/add_payment.html",{'form':form})