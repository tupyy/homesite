import calendar
from datetime import datetime

from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.utils import json

from money.models import Payment


class TotalViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated, ]

    def list(self, request):
        try:
            data = {}
            for month in range(1, datetime.now().month + 1):
                month_total_by_categories = Payment.totals.get_total_by_categories(month)
                month_total_by_categories["Total"] = float(Payment.totals.get_total(month))
                data[calendar.month_name[month]] = month_total_by_categories
            return HttpResponse(json.dumps(data), content_type='application/javascript; charset=utf8')
        except ValueError:
            return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            month = int(pk)
            data = Payment.totals.get_total(int(month))
            return HttpResponse(json.dumps({calendar.month_name[int(month)]: float(data)}),
                                content_type='application/javascript; charset=utf8')
        except ValueError:
            return Response("Bad month number", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path="total")
    def get_totals(self, request, pk=None):
        """
        Get the totals for a given month by subcategories
        :param request:
        :param pk: month id
        :return:
        """

        try:
            month = int(pk)
            if month not in range(1, 13):
                raise ValueError('Invalid month.')
            year = int(self.request.query_params.get("year", datetime.now().year))
        except ValueError as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        category_name = self.request.query_params.get("category")
        if category_name is None:
            category_total = Payment.totals.get_total_by_categories(month, year)
            return HttpResponse(json.dumps(category_total),
                                content_type='application/javascript; charset=utf8')
        else:
            total = Payment.totals.get_total_by_categories(month)
            category_total = total.get(category_name, 0)
            return HttpResponse(json.dumps(float(category_total)),
                                content_type='application/javascript; charset=utf8')

    @action(methods=['GET'], detail=False, url_path="year")
    def get_year_total(self, request):
        """
        Compute the totals for a certain year
        Route: api/money/total/year?year=2019
        :param request:
        :return: year total
        """
        try:
            year = self.request.query_params.get("year", datetime.now().year)
            year = int(year)
        except ValueError:
            return Response('Invalid year', status=status.HTTP_400_BAD_REQUEST)

        period_end = datetime.now().month + 1 if year == datetime.now().year else 12
        total = 0
        for i in range(1, period_end):
            total += float(Payment.totals.get_year_total(i, year))

        return HttpResponse(json.dumps(total),
                            content_type='application/javascript; charset=utf8')
