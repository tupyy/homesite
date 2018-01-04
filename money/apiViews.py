from models import Category,Subcategory,PaymentModel
from serialize import *
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

#TODO foloseste self.serializer_class
"""
    View sets for the serializers. Except CategoryViewSet they are not used for 
    moment
"""
class CategoryViewSet(viewsets.ViewSet):
    """
    View set for categories
    """
    permission_classes = (IsAuthenticated,)

    def create(self,request):
        serializer  = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        queryset = Category.objects.all()
        try:
            category = get_object_or_404(queryset, pk=pk)
            category.delete()
            return Response(CategorySerializer(category).data,status=status.HTTP_200_OK)
        except ValueError:
            return Response("Category with id " + pk + " not found", status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset,pk=pk)
        serializer = CategorySerializer(instance=category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        try:
            category = get_object_or_404(queryset, pk=pk)
            serializer = CategorySerializer(category)
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
            serializer  = SubcategorySerializer(data=request.data)
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
            return Response(SubcategorySerializer(subcategory).data, status=status.HTTP_200_OK)
        except ValueError:
            return Response("Category with id " + pk + " not found", status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        subcategory = get_object_or_404(Subcategory.objects.all(),pk=pk)
        try:
            serializer = SubcategorySerializer(instance=subcategory,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as ex:
            return Response(ex.detail,status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        queryset = Subcategory.objects.all()
        serializer = SubcategorySerializer(queryset,many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def category(self,request,pk=None):
        subcategory = get_object_or_404(Subcategory.objects.all(),pk=pk)
        return Response(CategorySerializer(subcategory.category).data,status=status.HTTP_200_OK)


class PaymentViewSet(viewsets.ViewSetMixin,generics.ListAPIView):
    serializer_class = PaymentModelSerialier

    def create(self,request):
        serializer = PaymentModelSerialier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @permission_classes((IsAuthenticated,))
    def destroy(self,request,pk=None):
        payment = get_object_or_404(PaymentModel,pk=pk)
        payment.delete()
        return Response(PaymentModelSerialier(payment).data,status=status.HTTP_200_OK)

    @permission_classes((IsAuthenticated,))
    def update(self,request,pk=None):
        payment = get_object_or_404(PaymentModel.objects.all(),pk=pk)

        try:
            serializer = PaymentModelSerialier(instance=payment,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as ex:
            return Response(ex.detail,status=status.HTTP_400_BAD_REQUEST)

    @permission_classes((IsAuthenticated,))
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
