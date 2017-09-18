# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_list_or_404
from forms import PaymentForm
from django.http import HttpResponseRedirect
from tables import MonthTable
from models import PaymentModel
# Create your views here.


def index(request):
    return render(request,'money/index.html')


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


def month_payments(request):
    table = MonthTable(PaymentModel.objects.all())

    return render(request,'money/month_payments.html',{'month_table':table})
