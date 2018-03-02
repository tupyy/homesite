# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from money.models import Category,Subcategory,PaymentModel,PaymentOption

# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(PaymentOption)


@admin.register(PaymentModel)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ('user','category','subcategory','sum','option_pay','nb_option','date','comments')
    exclude = ('id',)
    list_filter = ('category','subcategory','date')
    search_fields = ['category', 'subcategory','date']