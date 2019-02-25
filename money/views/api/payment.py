from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from authentication.permissions import IsPostOrIsAuthenticated
from money.models import Payment
from money.serializer.payment import PaymentSerializer


class PaymentViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
    serializer_class = PaymentSerializer

    # permission_classes = (IsPostOrIsAuthenticated,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return Response(self.serializer_class(payment).data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        payment = get_object_or_404(Payment.objects.all(), pk=pk)
        try:
            serializer = self.serializer_class(instance=payment, data=request.data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (serializers.ValidationError, KeyError) as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):

        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        _subcategory = self.request.query_params.get('subcategory', None)
        _category = self.request.query_params.get('category', None)
        _month = self.request.query_params.get('month', None)
        _year = self.request.query_params.get('year', None)

        if start_date and end_date:
            queryset = Payment.objects.filter(date__gte=start_date, date__lte=end_date)
        else:
            if _year:
                queryset = Payment.objects.filter(date__year=_year)
            else:
                queryset = Payment.objects.filter(date__year=datetime.now().year)
            if _month:
                queryset = queryset.filter(date__month=_month)

        if _subcategory and _category:
            queryset = queryset.filter(category__name__exact=_category,
                                       subcategory__name__exact=_subcategory,
                                       date__month=_month)
        elif _category and not _subcategory:
            queryset = queryset.filter(category__name__exact=_category,
                                       date__month=_month)
        return queryset
