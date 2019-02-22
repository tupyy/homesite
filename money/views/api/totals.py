import calendar

from django.http import HttpResponse, Http404
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
                month = int(m)
                if 0 < month < 13:
                    month_total_by_categories = Payment.totals.get_total_by_categories(month)
                    month_total_by_categories["Total"] = Payment.totals.get_total(month)
                    data[m] = month_total_by_categories
                else:
                    raise Http404
            return HttpResponse(json.dumps(data), content_type='application/javascript; charset=utf8')

        except ValueError:
            return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            month = int(pk)
            data = Payment.totals.get_total_by_categories(month)
            data["Total"] = Payment.totals.get_total(month)
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
            data = Payment.totals.get_total(int(month))
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
                data = Payment.totals.get_total(i)
                totals[calendar.month_name[i]] = data
            totals['revenues'] = str(Revenue.total.total())
            return HttpResponse(json.dumps(totals), content_type='application/javascript; charset=utf8')
        except ValueError:
            return Response('Bad month number', status=status.HTTP_400_BAD_REQUEST)
