from rest_framework import serializers
from django.shortcuts import get_object_or_404
from datetime import datetime
from money.models import *


class SubcategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    id = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        if self.__get_category_name() is not None:
            category = Category.objects.filter(name__exact=self.__get_category_name())
            if len(category) == 0:
                raise serializers.ValidationError('Category ' + self.__get_category_name() + ' is not found')
            (obj, created) = Subcategory.objects.get_or_create(category=category[0], name=validated_data['name'],
                                                               description=validated_data['description'])
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

            instance.name = validated_data.get('name', instance.name)
            instance.description = validated_data.get('description', instance.description)
            instance.save()
            return instance

    class Meta:
        model = Subcategory
        fields = ('id', 'category', 'name', 'description')

    def __get_category_name(self):
        try:
            return self.initial_data['category']
        except KeyError:
            return None

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category
    """
    subcategories = SubcategorySerializer(read_only=True, many=True)
    id = serializers.IntegerField(read_only=True)

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



class PaymentSerialier(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    contract = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ('__all__')

    def create(self, validated_data):
        try:
            category = self.__get_category(self.initial_data['category'])
            subcategory = self.__get_subcategory(self.initial_data['subcategory'])

            if self.__is_valid_subcategory(category.name, subcategory.name):
                user = self.__get_user(self.initial_data['user'])

                payment = Payment.objects.create(user=user,
                                                 category=category,
                                                 subcategory=subcategory,
                                                 sum=float(validated_data['sum']),
                                                 date=validated_data['date'],
                                                 nb_tickete=int(validated_data['nb_tickete']),
                                                 comments=validated_data['comments'])
                return payment
            else:
                raise serializers.ValidationError(
                    'Subcategory %s does not belong to category %s' % (subcategory.name, category.name))
        except (IndexError, KeyError, ValueError) as ex:
            raise serializers.ValidationError(ex.message)

    def update(self, instance, validated_data):
        try:
            category = self.__get_category(self.initial_data['category'])
            subcategory = self.__get_subcategory(self.initial_data['subcategory'])

            if self.__is_valid_subcategory(category.name, subcategory.name):
                user = self.__get_user(self.initial_data['user'])

                instance.category = category
                instance.user = user
                instance.subcategory = subcategory
                instance.sum = validated_data.get("sum", instance.sum)
                instance.nb_tickete = validated_data.get('nb_tickete', instance.nb_tickete)
                instance.date = validated_data.get('date', instance.date)
                instance.comments = validated_data.get('comments', instance.comments)
                instance.save()
                return instance
            else:
                raise serializers.ValidationError(
                    'Subcategory %s does not belong to category %s' % (subcategory.name, category.name))
        except (IndexError, KeyError) as ex:
            raise serializers.ValidationError(ex.message)

    def __is_valid_subcategory(self, category_name, subcategory_name):
        """
        Check if the subcategory belongs to the category
        :param category_name:
        :param subcategory_name:
        :return: true if the subcategory belongs to the category
        """
        category = self.__get_category(category_name)
        subcategory = self.__get_subcategory(subcategory_name)
        if category.pk == subcategory.category.pk:
            return True

        return False

    def __get_category(self, category_name):
        return Category.objects.filter(name__exact=category_name)[0]

    def __get_subcategory(self, subcategory):
        return Subcategory.objects.filter(name__exact=subcategory)[0]

    def __get_user(self, username):
        return User.objects.filter(username__exact=username)[0]

    def __get_contract(self, contract_id):
        return User.objects.filter(contract_id__exact=contract_id)[0]


class TotalSerializer(serializers.Serializer):
    total = serializers.DictField()

