from models import Category,Subcategory,PaymentModel
from serialize import *
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

"""
    View sets for the serializers. Except CategoryViewSet they are not used for 
    moment
"""
class CategoryViewSet(viewsets.ViewSet):
    """
    View set for categories
    """
    def list(self,request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class SubcategoryViewSet(viewsets.ViewSet):
    """
    Viewset for subcategory
    """
    def list(self,request):
        queryset = Subcategory.objects.all()
        serializer = SubcategorySerializer(queryset,many=True)
        return Response(serializer.data)


class SubcategoryList(generics.ListAPIView):
    """
    Filter the subcategory objects based on category
    """
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        category_name = self.kwargs['category']
        return Subcategory.objects.filter(category__name__exact=category_name)


class PaymentViewSet(viewsets.ViewSet):
    """
    Payment view set
    """
    def list(self,request):
        queryset = PaymentModel.objects.all()
        serializer = PaymentModelSerialier(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = PaymentModel.objects.all()
        payment_model = get_object_or_404(queryset, pk=pk)
        serializer = PaymentModelSerialier(payment_model)
        return Response(serializer.data)