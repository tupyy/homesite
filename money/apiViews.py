import calendar
import json

from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
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

        category_name = self.request.query_params.get("category")
        if category_name is None:
            return Response("Category is null", status=status.HTTP_400_BAD_REQUEST)
        else:
            payments = Payment.objects.filter(date__month=pk, category__name__exact=category_name)

            subcategory_total = dict()
            subcategories = Subcategory.objects.filter(category__name__exact=category_name)

            total1 = 0
            for subcategory in subcategories:
                total = 0
                for payment in payments:
                    if payment.subcategory.name == subcategory.name:
                        total += payment.sum
                total1 += total
                subcategory_total[subcategory.name] = str(total)

            # check if we have some total <> 0
            if total1 == 0:
                subcategory_total = dict()

            return HttpResponse(
                json.dumps(subcategory_total),
                content_type='application/javascript; charset=utf8'
            )

    @action(methods=['GET'], detail=True, url_path="year_total")
    def get_year_total(self, request, pk=None):
        """
        Compute the totals for each month of the current year for each subcategory
        :param request:
        :param pk: category name
        :return:
        """

        subcategory_total = dict()

        subcategories = Subcategory.objects.filter(category__name__exact=pk)
        titles = []
        for subcategory in subcategories:
            titles.append(subcategory.name)

        subcategory_total['subcategories'] = titles
        for month in range(1, datetime.today().month + 1):
            month_total = []
            for subcategory in subcategories:
                total = 0
                payments = Payment.objects.filter(date__year=datetime.today().year,
                                                  date__month=month,
                                                  category__name__exact=pk,
                                                  subcategory__name__exact=subcategory.name)
                for payment in payments:
                    total += payment.sum

                month_total.append(str(total))
            subcategory_total[calendar.month_name[month]] = month_total

        # check if we have some total <> 0

        return HttpResponse(
            json.dumps(subcategory_total),
            content_type='application/javascript; charset=utf8'
        )


class SubcategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
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

    @action(methods=['get'], detail=True)
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
    # permission_classes = [IsAuthenticated, ]

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
            return HttpResponse(json.dumps({calendar.month_name[int(month)]: data}), content_type='application/javascript; charset=utf8')
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
            last_month = int(pk)
            totals = dict()
            for i in range(1, last_month + 1):
                data = Payment.totals.compute_total2(i)
                totals[calendar.month_name[i]] = data
            return HttpResponse(json.dumps(totals),content_type='application/javascript; charset=utf8')
        except ValueError:
            return Response('Bad month number', status=status.HTTP_400_BAD_REQUEST)
