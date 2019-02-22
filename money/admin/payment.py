# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from contract.models import Contract
from money.models import Payment, RecurrentPayment, PaymentOccurrence


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'subcategory', 'sum', 'date', 'comments')
    exclude = ('id',)
    list_filter = ('category', 'subcategory', 'date')
    search_fields = ['category', 'subcategory', 'date']


@admin.register(RecurrentPayment)
class RecurrentPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'subcategory', 'sum', 'date', 'comments', 'get_name')
    exclude = ('id',)
    list_filter = ('category', 'subcategory', 'date')
    search_fields = ['category', 'subcategory', 'date']

    def get_name(self, obj):
        return obj.contract.name

    get_name.admin_order_field = 'contract'  # Allows column order sorting
    get_name.short_description = 'Contract Name'  # Renames column head

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "contract":
            kwargs["queryset"] = Contract.objects.filter(status__status__exact="Open")
        return super(RecurrentPaymentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PaymentOccurrence)
class PaymentOccurrence(admin.ModelAdmin):
    list_display = ("start", "end", "repeat", "get_name", "get_payment_id")

    def get_payment_id(self,obj):
        return obj.payment.id

    def get_name(self,obj):
        return obj.payment.contract.name

    get_name.short_description = 'Contract name'
    get_payment_id.short_description = 'Payment ID'
