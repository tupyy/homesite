from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from money.models import Category, Subcategory
from money.serializer import CategorySerializer, SubcategorySerializer

"""
    View sets for the serializers. Except CategoryViewSet they are not used for 
    moment
"""


class CategoryViewSet(viewsets.ViewSet):
    """
    View set for categories
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
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


class SubcategoryViewSet(viewsets.ViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
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
