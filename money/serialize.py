from rest_framework import serializers
from django.shortcuts import get_object_or_404
from models import *


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category
    """
    subcategories = serializers.StringRelatedField(read_only=True,many=True)
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        (obj,created) = Category.objects.get_or_create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        """
        Update and return an existing Category instance
        :param instance:
        :type instance Category
        :param validated_data:
        :return:
        """
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.save()
        return instance
    class Meta:
        model = Category
        fields = ('id','name','description','subcategories')


class SubcategorySerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField(read_only=True)
    id = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        if self.__get_category_name() is not None:
            category = Category.objects.filter(name__exact=self.__get_category_name())
            if len(category) == 0:
                raise serializers.ValidationError('Category ' + self.__get_category_name() + ' is not found')
            (obj,created) = Subcategory.objects.get_or_create(category=category[0],name=validated_data['name'],description=validated_data['description'])
            return obj
        else:
            raise serializers.ValidationError('Category not found')

    def update(self, instance, validated_data):
        """
        Update and return an existing Subcategory instance
        :param instance:
        :type instance Subcategory
        :param validated_data:
        :return:
        """

        if self.__get_category_name() is not None:
            category = Category.objects.filter(name__exact=self.__get_category_name())
            if len(category) > 0:
                if category[0].name != instance.category.name:
                    instance.category = category[0]
            else:
                raise serializers.ValidationError("New category not found")

            instance.name = validated_data.get('name',instance.name)
            instance.description = validated_data.get('description',instance.description)
            instance.save()
            return instance

    class Meta:
        model = Subcategory
        fields = ('id','category','name','description')

    def __get_category_name(self):
        try:
            return self.initial_data['category']
        except KeyError:
            return None


class PaymentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOption
        fields = ('__all__')


class PaymentModelSerialier(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category_name')
    subcategory = serializers.SerializerMethodField('get_subcategory_name')
    user = serializers.SerializerMethodField('get_username')

    class Meta:
        model = PaymentModel
        fields = ('__all__')

    def create(self, validated_data):
        pass

    def get_category_name(self,payment):
        ":type payment PaymentModel"
        return payment.category.name

    def get_subcategory_name(self,payment):
        ":type payment PaymentModel"
        return payment.subcategory.name

    def get_username(self,payment):
        ":type payment PaymentModel"
        return payment.user.name


