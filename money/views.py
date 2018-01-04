# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# import datetime
#
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
#
# from forms import PaymentForm,PermanentPaymentForm
# from serialize import *
# from tables import MonthTable, TotalTable,ViewPermanentPaymentTable
# from utils import compute_total
# from datetime import date
#
# """
#     Djano classic view
# """
#
# def index(request):
#     payments = PaymentModel.objects.filter(date__month=datetime.date.today().month)
#     data = compute_total(payments,Category.objects.all())
#     table = TotalTable(data)
#     return render(request, 'money/index.html', {'total_table' : table})
#
#
#
# def payment(request):
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             if 'submit' in request.POST:
#                 form = PaymentForm()
#             else:
#                 return HttpResponseRedirect('/')
#     else:
#         form = PaymentForm()
#     return render(request,'money/payment.html',{'form': form})
#
#
# def permanent_payment(request):
#     if request.method == 'POST':
#         form = PermanentPaymentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             if 'submit' in request.POST:
#                 form = PermanentPaymentForm()
#             else:
#                 return HttpResponseRedirect('/')
#     else:
#         form = PermanentPaymentForm()
#     return render(request,'money/payment.html',{'form': form})
#
# @login_required
# def delete_payment(request,pk):
#     """
#     Delete a payment
#     :param request:
#     :param pk: PrimaryKey
#     :return:
#     """
#     payment = get_object_or_404(PaymentModel,pk=pk)
#     payment.delete()
#     return HttpResponseRedirect('/month')
#
# @login_required
# def delete_permanent_payment(request,pk):
#     """
#     Delete a permanent paymen
#     :param request:
#     :param pk:
#     :return:
#     """
#     payment=get_object_or_404(PermanentPaymentModel,pk=pk)
#     payment.delete()
#     return HttpResponseRedirect('/view_permanent_payments')
#
# @login_required
# def month_payments(request):
#     table = MonthTable(PaymentModel.objects.filter(date__month=datetime.date.today().month))
#     return render(request,'money/month_payments.html',{'month_table':table,
#                                                        'nav_bar_title':datetime.date.today().strftime('%B') + " payments"
#                                                        })
#
# @login_required
# def view_permanent_payments(request):
#     table = ViewPermanentPaymentTable(PermanentPaymentModel.objects.all())
#     return render(request,'money/month_payments.html' ,{'month_table':table,
#                                                         'nav_bar_title':'Viramente periodice lunare'
#                                                         })
