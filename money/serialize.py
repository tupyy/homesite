from rest_framework import serializers
from django.shortcuts import get_object_or_404
from datetime import datetime
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
    id = serializers.IntegerField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    option_pay = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PaymentModel
        fields = ('__all__')

    def create(self, validated_data):
        try:
            category = self.__get_category(self.initial_data['category'])
            subcategory = self.__get_subcategory(self.initial_data['subcategory'])
            payment_option = self.__get_payment_option(self.initial_data['payment_option'])
            user = self.__get_user(self.initial_data['user'])

            (payment,created) = PaymentModel.objects.get_or_create(user=user,category=category,
                                                         subcategory=subcategory,
                                                         sum=float(validated_data['sum']),
                                                         date = validated_data['date'],
                                                         option_pay=payment_option,
                                                         nb_option = int(validated_data['nb_option']),
                                                         comments = validated_data['comments'])
            return payment
        except (IndexError,KeyError,ValueError) as ex:
            raise serializers.ValidationError(ex.message)
        
    def __get_category(self,category_name):
        return Category.objects.filter(name__exact=category_name)[0]

    def __get_subcategory(self,subcategory):
        return Subcategory.objects.filter(name__exact=subcategory)[0]

    def __get_user(self,username):
        return User.objects.filter(username__exact=username)[0]

    def __get_payment_option(self,payment_option):
        return PaymentOption.objects.filter(name__exact=payment_option)[0]

    # def get_category_name(self,payment):
    #     ":type payment PaymentModel"
    #     return payment.category.name
    #
    # def get_subcategory_name(self,payment):
    #     ":type payment PaymentModel"
    #     return payment.subcategory.name
    #
    # def get_username(self,payment):
    #     ":type payment PaymentModel"
    #     return payment.user.name


