# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from contract.models import Contract
from money.models import Category, Subcategory, Payment, RecurrentPayment, PaymentOccurrence

# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(PaymentOccurrence)


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'subcategory', 'sum', 'nb_tickete', 'date', 'comments')
    exclude = ('id',)
    list_filter = ('category', 'subcategory', 'date')
    search_fields = ['category', 'subcategory', 'date']


@admin.register(RecurrentPayment)
class RecurrentPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'subcategory', 'sum', 'date', 'comments')
    exclude = ('id',)
    list_filter = ('category', 'subcategory', 'date')
    search_fields = ['category', 'subcategory', 'date']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "contract":
            kwargs["queryset"] = Contract.objects.filter(status__status__exact="Active")
        return super(RecurrentPaymentAdmin ,self).formfield_for_foreignkey(db_field, request, **kwargs)


