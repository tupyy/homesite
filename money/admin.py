# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from money.models import Category,Subcategory,Payment

# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ('user','category','subcategory','sum','nb_tickete','date','comments')
    exclude = ('id',)
    list_filter = ('category','subcategory','date')
    search_fields = ['category', 'subcategory','date']