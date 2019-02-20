import calendar

from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.utils import json

from money.models import Payment, Revenue


class TotalViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated, ]

    def list(self, request):
        try:
            data = {}
            months = request.GET.get("month", "").split(",")

            for m in months:
                month_index = int(m)
                if 0 < month_index < 13:
                    month_data = Payment.totals.compute_categories(month_index)
                    month_data["Total"] = Payment.totals.compute_total2(month_index)
                    data[m] = month_data

            return HttpResponse(json.dumps(data), content_type='application/javascript; charset=utf8')

        except ValueError:
            return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            month = int(pk)
            data = Payment.totals.compute_categories(month)
            data["Total"] = Payment.totals.compute_total2(month)
            return HttpResponse(
                json.dumps(data),
                content_type='application/javascript; charset=utf8'
            )
        except ValueError:
            return Response('Bad month number', status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True, url_path="month_total")
    def get_month_total(self, request, pk=None):
        try:
            month = int(pk)
            data = Payment.totals.compute_total2(int(month))
            return HttpResponse(json.dumps({calendar.month_name[int(month)]: data}),
                                content_type='application/javascript; charset=utf8')
        except ValueError:
            return Response("Bad month number", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True, url_path="months_total")
    def get_months_total(self, request, pk=None):
        """
        Compute the totals for each month prior to pk
        :param request:
        :param pk: last month
        :return:
        """
        try:

            total_revenues = Revenue.total.total()

            last_month = int(pk)
            totals = dict()
            for i in range(1, last_month + 1):
                data = Payment.totals.compute_total2(i)
                totals[calendar.month_name[i]] = data
            totals['revenues'] = str(Revenue.total.total())
            return HttpResponse(json.dumps(totals), content_type='application/javascript; charset=utf8')
        except ValueError:
            return Response('Bad month number', status=status.HTTP_400_BAD_REQUEST)
