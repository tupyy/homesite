import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from money.models import Category, Payment, Subcategory
from money.serializer import CategorySerializer, SubcategorySerializer

"""
    View sets for the serializers. Except CategoryViewSet they are not used for 
    moment
"""


class CategoryViewSet(viewsets.ViewSet):
    """
    View set for categories
    """
    # permission_classes = (IsAuthenticated,)
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
            if month < 0 or month > 12:
                raise ValueError
        except ValueError:
            return Response('month value invalid', status=status.HTTP_400_BAD_REQUEST)

        category_name = self.request.query_params.get("category")
        if category_name is None:
            total = Payment.totals.get_total_by_categories(month)
            category_total = {k: float(v) for k, v in total.items()}
            return HttpResponse(json.dumps(category_total),
                                content_type='application/javascript; charset=utf8')
        else:
            total = Payment.totals.get_total_by_categories(month)
            category_total = total.get(category_name, 0)
            return HttpResponse(
                json.dumps(float(category_total)),
                content_type='application/javascript; charset=utf8'
            )

    @action(methods=['GET'], detail=True, url_path="year_total")
    def get_year_total(self, request, pk=None):
        """
        Compute the totals for each month of the current year for each subcategory
        Route: api/money/category/casa/year_total?year=2019
        :param request:
        :param pk: category name
        :return: the total spending for a category from the beginning of the year to the current month if the
                 year is the current year. Otherwise return the total of a whole year
        """
        try:
            _ = Category.objects.get(name=pk)
        except Category.DoesNotExist:
            return Response("Category do noy exists.", status=status.HTTP_404_NOT_FOUND)

        try:
            year = self.request.query_params.get("year", datetime.now().year)
        except ValueError:
            return Response('Invalid year', status=status.HTTP_400_BAD_REQUEST)

        period_end = datetime.now().month + 1 if year == datetime.now().year else 12
        total = 0
        for i in range(1, period_end):
            total += float(Payment.totals.get_category_total(pk, i, year))

        return HttpResponse(
            json.dumps(total),
            content_type='application/javascript; charset=utf8'
        )


class SubcategoryViewSet(viewsets.ViewSet):
    # permission_classes = (IsAuthenticated,)
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
            return Response("Subcategory with id " + pk + " not found", status=status.HTTP_400_BAD_REQUEST)

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
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        subcategory = Subcategory.objects.filter(category__name__exact=pk)
        return Response(CategorySerializer(subcategory[0].category).data, status=status.HTTP_200_OK)
