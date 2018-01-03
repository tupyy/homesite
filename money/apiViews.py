from models import Category,Subcategory,PaymentModel
from serialize import *
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

"""
    View sets for the serializers. Except CategoryViewSet they are not used for 
    moment
"""
class CategoryViewSet(viewsets.ViewSet):
    """
    View set for categories
    """
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

    def get_queryset(self):
        category_name = self.kwargs['category']
        return Subcategory.objects.filter(category__name__exact=category_name)


class PaymentViewSet(viewsets.ViewSetMixin,generics.ListAPIView):
   serializer_class = PaymentModelSerialier

   def get_queryset(self):
       queryset = PaymentModel.objects.all()
       start_date = self.request.query_params.get('start_date',None)
       end_date = self.request.query_params.get('end_date',None)
       if start_date is not None and end_date is not None:
           queryset = queryset.filter(date__gte=start_date,date__lte=end_date)
       return queryset


