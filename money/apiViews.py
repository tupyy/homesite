from django.contrib.auth.decorators import login_required

from money.models import Category,Subcategory,PaymentModel
from money.serialize import *
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsPostOrIsAuthenticated
from rest_framework.decorators import permission_classes

#TODO foloseste self.serializer_class
from money.utils import compute_total, append_to_total

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

    def create(self,request):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        queryset = Category.objects.all()
        try:
            category = get_object_or_404(queryset, pk=pk)
            category.delete()
            return Response(self.serializer_class(category).data,status=status.HTTP_200_OK)
        except ValueError:
            return Response("Category with id " + pk + " not found", status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset,pk=pk)
        serializer = self.serializer_class(instance=category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
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
            return Response("Argument must be an int",status=status.HTTP_400_BAD_REQUEST)


class SubcategoryViewSet(viewsets.ViewSet,generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubcategorySerializer

    """
    Viewset for subcategory
    """
    def create(self,request):

        try:
            serializer  = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
        except serializers.ValidationError as ex:
            return Response(ex.detail,status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk):
        queryset = Subcategory.objects.all()
        try:
            subcategory = get_object_or_404(queryset, pk=pk)
            subcategory.delete()
            return Response(self.serializer_class(subcategory).data, status=status.HTTP_200_OK)
        except ValueError:
            return Response("Category with id " + pk + " not found", status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        subcategory = get_object_or_404(Subcategory.objects.all(),pk=pk)
        try:
            serializer = self.serializer_class(instance=subcategory,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as ex:
            return Response(ex.detail,status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        queryset = Subcategory.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def category(self,request,pk=None):
        subcategory = get_object_or_404(Subcategory.objects.all(),pk=pk)
        return Response(CategorySerializer(subcategory.category).data,status=status.HTTP_200_OK)


class PaymentViewSet(viewsets.ViewSetMixin,generics.ListAPIView):
    serializer_class = PaymentModelSerialier
    permission_classes = (IsPostOrIsAuthenticated,)

    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        payment = get_object_or_404(PaymentModel,pk=pk)
        payment.delete()
        return Response(self.serializer_class(payment).data,status=status.HTTP_200_OK)

    def update(self,request,pk=None):
        payment = get_object_or_404(PaymentModel.objects.all(),pk=pk)

        try:
            serializer = self.serializer_class(instance=payment,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as ex:
            return Response(ex.detail,status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
       queryset = PaymentModel.objects.all()
       start_date = self.request.query_params.get('start_date',None)
       end_date = self.request.query_params.get('end_date',None)
       if start_date is not None and end_date is not None:
           queryset = queryset.filter(date__gte=start_date,date__lte=end_date)
       return queryset


class PaymentOptionViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    
    def create(self,request):
        serializer = PaymentOptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self,request,pk=None):
        queryset = PaymentOption.objects.all()
        try:
            payment_option = get_object_or_404(queryset, pk=pk)
            payment_option.delete()
            return Response(PaymentOptionSerializer(payment_option).data,status=status.HTTP_200_OK)
        except ValueError:
            return Response("Payment option with id " + pk + " not found", status=status.HTTP_400_BAD_REQUEST)


    def update(self,request,pk=None):
        queryset = PaymentOption.objects.all()
        payment_option = get_object_or_404(queryset,pk=pk)
        serializer = PaymentOptionSerializer(instance=payment_option,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def list(self,request):
        queryset = PaymentOption.objects.all()
        serializer = PaymentOptionSerializer(queryset, many=True)
        return Response(serializer.data)


class TotalViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated,]

    def retrieve(self,request,pk=None):
        payments = PaymentModel.objects.filter(date__month=pk)
        data = compute_total(payments, Category.objects.all())

        # Compute totals for n-1 and n-2 month
        try:
            month = int(pk)
            if month > 2:
                prev_month_limit = 2
            else:
                prev_month_limit = 1

            for i in range(month - prev_month_limit, month):
                payments_prev = PaymentModel.objects.filter(date__month=i)
                data_previous_month = compute_total(payments_prev, Category.objects.all())
                append_to_total(data, data_previous_month, i)

            serializer = TotalSerializer(data, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response(e.__str__(), status=status.HTTP_400_BAD_REQUEST)