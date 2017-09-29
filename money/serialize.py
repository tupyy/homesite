from rest_framework import serializers
from django.shortcuts import get_object_or_404
from models import *


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category
    """
    subcategories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ('id','name','description','subcategories')


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id','category','name','description')


class PaymentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOption
        fields = ('__all__')


class PaymentModelSerialier(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = ('__all__')



