from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.utils import json

from money.models import Revenue


class RevenuesViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated, ]

    @action(methods=['GET'], detail=False, url_path='total_revenues')
    def get_revenues_total(self, request):
        data = Revenue.total.total()
        return HttpResponse(json.dumps({'revenues': str(data)}), content_type='application/javascript; charset=utf8')