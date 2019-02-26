from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from money.models import Category, Subcategory


class SubcategorySerializer(serializers.Serializer):
    category = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)

    def create(self, validated_data):
        if self.is_valid(raise_exception=True):
            category = Category.objects.filter(name__exact=self.validated_data['category']).first()
            (obj, created) = Subcategory.objects.get_or_create(category=category,
                                                               name=validated_data['name'],
                                                               description=validated_data.get('description', None))
            return obj

    def update(self, instance, validated_data):
        """
        Update and return an existing Subcategory instance
        :param instance:
        :type instance Subcategory
        :param validated_data:
        :return:
        """

        if self.is_valid(raise_exception=True):
            category = Category.objects.filter(name__exact=self.__get_category_name()).first()
            instance.category = category
            instance.name = validated_data.get('name', instance.name)
            instance.description = validated_data.get('description', instance.description)
            instance.save()
            return instance

    class Meta:
        model = Subcategory

    def validate_category(self, value):
        try:
            _ = Category.objects.get(name__exact=value)
            return value
        except Http404:
            raise ValidationError('Category {} do not exists.'.format(value))


class CategorySerializer(serializers.Serializer):
    """
    Serializer for Category
    """
    subcategories = SubcategorySerializer(read_only=True, many=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)

    def create(self, validated_data):
        (obj, created) = Category.objects.get_or_create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        """
        Update and return an existing Category instance
        :param instance:
        :type instance Category
        :param validated_data:
        :return:
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'subcategories')
