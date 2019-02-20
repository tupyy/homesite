import calendar
from datetime import date

from django.shortcuts import render

from money import utils
from money.models import Category


def index(request):
    months_choices = []
    for i in range(1, date.today().month + 1):
        months_choices.append(calendar.month_name[i])

    next_payments = utils.get_future_payments()

    return render(request, 'index.html', {'luni': months_choices,
                                          'next_payments': next_payments})


def category_total(request):

    months_choices = []
    for i in range(1, date.today().month + 1):
        months_choices.append(calendar.month_name[i])

    return render(request, "money/category_total.html", {
        'luni': months_choices,
        'categorii': Category.objects.all(),
    })