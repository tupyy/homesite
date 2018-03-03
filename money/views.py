# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
import calendar
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

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
            if 'submit' in request.POST:
                form = PaymentForm()
            else:
                return HttpResponseRedirect('/')
    else:
        form = PaymentForm()
    return render(request,'money/payment.html',{'form': form})


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
def delete_payment(request,pk):
    """
    Delete a payment
    :param request:
    :param pk: PrimaryKey
    :return:
    """
    payment = get_object_or_404(PaymentModel,pk=pk)
    payment.delete()
    return HttpResponseRedirect('/month')

@login_required
def delete_permanent_payment(request,pk):
    """
    Delete a permanent paymen
    :param request:
    :param pk:
    :return:
    """
    payment=get_object_or_404(PermanentPaymentModel,pk=pk)
    payment.delete()
    return HttpResponseRedirect('/view_permanent_payments')

@login_required
def month_payments(request):
    table = MonthTable(PaymentModel.objects.filter(date__month=date.today().month))
    return render(request,'money/month_payments.html',{'month_table':table,
                                                       'nav_bar_title':date.today().strftime('%B') + " payments"
                                                       })

@login_required
def view_permanent_payments(request):
    table = ViewPermanentPaymentTable(PermanentPaymentModel.objects.all())
    return render(request,'money/month_payments.html' ,{'month_table':table,
                                                        'nav_bar_title':'Viramente periodice lunare'
                                                        })

