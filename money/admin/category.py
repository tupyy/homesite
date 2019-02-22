# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from money.models import Category, Subcategory

# Register your models here.
admin.site.register(Category)


@admin.register(Subcategory)
class SubcategoryAdminModel(admin.ModelAdmin):
    list_display = ("name", 'get_category')
    search_fields = ['get_category']
    list_filter = ("category",)

    def get_category(self, obj):
        return obj.category.name

    get_category.short_description = "Category"
    get_category.admin_order_field = "category"
