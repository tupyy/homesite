from django.contrib.auth.models import User
from rest_framework import serializers

from money.models import *


class PaymentSerializer(serializers.ModelSerializer):
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

