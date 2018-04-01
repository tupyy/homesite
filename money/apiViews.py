import json

from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.permissions import IsPostOrIsAuthenticated
from money.serialize import *

"""
    View sets for the serializers. Except CategoryViewSet they are not used for 
    moment
"""


class CategoryViewSet(viewsets.ViewSet):
    """
    View set for categories
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Category.objects.all()
        try:
            category = get_object_or_404(queryset, pk=pk)
            category.delete()
            return Response(self.serializer_class(category).data, status=status.HTTP_200_OK)
        except ValueError:
            return Response("Category with id " + pk + " not found", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Category.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        try:
            category = get_object_or_404(queryset, pk=pk)
            serializer = self.serializer_class(category)
            return Response(serializer.data)
        except ValueError:
            return Response("Argument must be an int", status=status.HTTP_400_BAD_REQUEST)


class SubcategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubcategorySerializer

    """
    Viewset for subcategory
    """

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as ex:
            return Response(ex.detail, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        queryset = Subcategory.objects.all()
        try:
            subcategory = get_object_or_404(queryset, pk=pk)
            subcategory.delete()
            return Response(self.serializer_class(subcategory).data, status=status.HTTP_200_OK)
        except ValueError:
            return Response("Category with id " + pk + " not found", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        subcategory = get_object_or_404(Subcategory.objects.all(), pk=pk)
        try:
            serializer = self.serializer_class(instance=subcategory, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as ex:
            return Response(ex.detail, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Subcategory.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def category(self, request, pk=None):
        subcategory = Subcategory.objects.filter(category__name__exact=pk)
        return Response(CategorySerializer(subcategory[0].category).data, status=status.HTTP_200_OK)


class PaymentViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
    serializer_class = PaymentSerialier

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


class TotalViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]

    def retrieve(self, request, pk=None):
        try:
            month = int(pk)
            data = Payment.totals.compute_categories(month)
            return HttpResponse(
                json.dumps(data),
                content_type='application/javascript; charset=utf8'
            )
        except ValueError:
            return Response('Bad month number', status=status.HTTP_400_BAD_REQUEST)
