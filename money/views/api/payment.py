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

    permission_classes = (IsPostOrIsAuthenticated,)

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
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as ex:
            return Response(ex.detail, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):

        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        subcategorie = self.request.query_params.get('subcategory', None)
        category = self.request.query_params.get('category', None)
        month = self.request.query_params.get('month', None)

        if start_date is not None and end_date is not None:
            queryset = Payment.objects.filter(date__gte=start_date, date__lte=end_date)
        elif subcategorie is not None and category is not None and month is not None:
            if subcategorie == "all":
                queryset = Payment.objects.filter(category__name__exact=category,
                                                  date__month=month)
            else:
                queryset = Payment.objects.filter(subcategory__name__exact=subcategorie,
                                                  category__name__exact=category,
                                                  date__month=month)
        elif month is not None:
            queryset = Payment.objects.filter(date__month=month)
        else:
            return []

        return queryset


