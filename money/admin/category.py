# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from money.models import Category, Subcategory

# Register your models here.
admin.site.register(Category)


@admin.register(Subcategory)
class SubcategoryAdminModel(admin.ModelAdmin):
    pass