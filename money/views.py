# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

from forms import PaymentForm,PermanentPaymentForm
from serialize import *
from tables import MonthTable, TotalTable,ViewPermanentPaymentTable
from utils import compute_total
from datetime import date

"""
    View sets for the serializers. Except CategoryViewSet they are not used for 
    moment
"""
class CategoryViewSet(viewsets.ViewSet):
    """
    View set for categories
    """
    def list(self,request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class SubcategoryViewSet(viewsets.ViewSet):
    """
    Viewset for subcategory
    """
    def list(self,request):
        queryset = Subcategory.objects.all()
        serializer = SubcategorySerializer(queryset,many=True)
        return Response(serializer.data)


class SubcategoryList(generics.ListAPIView):
    """
    Filter the subcategory objects based on category
    """
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        category_name = self.kwargs['category']
        return Subcategory.objects.filter(category__name__exact=category_name)


class PaymentViewSet(viewsets.ViewSet):
    """
    Payment view set
    """
    def list(self,request):
        queryset = PaymentModel.objects.all()
        serializer = PaymentModelSerialier(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = PaymentModel.objects.all()
        payment_model = get_object_or_404(queryset, pk=pk)
        serializer = PaymentModelSerialier(payment_model)
        return Response(serializer.data)


"""
    Djano classic view
"""

def index(request):
    payments = PaymentModel.objects.filter(date__month=datetime.date.today().month)
    data = compute_total(payments,Category.objects.all())
    table = TotalTable(data)
    return render(request, 'money/index.html', {'total_table' : table})



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
    table = MonthTable(PaymentModel.objects.filter(date__month=datetime.date.today().month))
    return render(request,'money/month_payments.html',{'month_table':table,
                                                       'nav_bar_title':datetime.date.today().strftime('%B') + " payments"
                                                       })

@login_required
def view_permanent_payments(request):
    table = ViewPermanentPaymentTable(PermanentPaymentModel.objects.all())
    return render(request,'money/month_payments.html' ,{'month_table':table,
                                                        'nav_bar_title':'Viramente periodice lunare'
                                                        })
