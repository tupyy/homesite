from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from money.models import *


class PaymentSerializer(serializers.Serializer):
    category = serializers.CharField(required=True)
    subcategory = serializers.CharField(required=True)
    user = serializers.CharField(required=True)
    sum = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    date = serializers.DateField(required=True)
    comments = serializers.StringRelatedField()

    def create(self, validated_data):
        try:
            _category = get_object_or_404(Category.objects.all(), name=self.initial_data['category'])
            _subcategory = Subcategory.objects.filter(name=self.initial_data['subcategory'],
                                                      category__name=_category.name).first()
            _user = get_object_or_404(User.objects.all(), username=self.initial_data['user'])
            if self.is_valid():
                _payment = Payment.objects.create(user=_user,
                                                  category=_category,
                                                  subcategory=_subcategory,
                                                  sum=float(validated_data['sum']),
                                                  date=validated_data['date'],
                                                  comments=validated_data.get('comments', ''))
                return _payment
        except (ValueError, Http404) as ex:
            raise serializers.ValidationError(str(ex))
        except KeyError as err:
            raise serializers.ValidationError('Field missing: ' + str(err))

    def update(self, instance, validated_data):
        try:
            _category = get_object_or_404(Category.objects.all(), name=self.initial_data['category'])
            _subcategory = get_object_or_404(Subcategory.objects.all(), name=self.initial_data['subcategory'])

            if self.__is_valid_subcategory(_category.name, _subcategory.name):
                user = get_object_or_404(User.objects.all(), username=self.initial_data['user'])

                instance.category = _category
                instance.user = user
                instance.subcategory = _subcategory
                instance.sum = validated_data.get("sum", instance.sum)
                instance.date = validated_data.get('date', instance.date)
                instance.comments = validated_data.get('comments', instance.comments)
                instance.save()
                return instance
            else:
                raise serializers.ValidationError(
                    'Subcategory %s does not belong to category %s' % (_subcategory.name, _category.name))
        except (ValueError, Http404) as ex:
            raise serializers.ValidationError(str(ex))
        except KeyError as err:
            raise serializers.ValidationError('Field missing: ' + str(err))

    def validate_category(self, value):
        try:
            _category = get_object_or_404(Category, name=self.initial_data['category'])
            return value
        except Http404:
            raise ValidationError('Category {} do not exists.'.format(self.initial_data['category']))

    def validate_subcategory(self, value):
        if not value:
            raise ValidationError('Subcategory not present')
        _subcategory = Subcategory.objects.filter(name=value,
                                                  category__name__exact=self.initial_data['category']).first()
        if not _subcategory:
            raise ValidationError('Subcategory {} is not part of category {}'.format(value, self.initial_data['category']))
        return value


class TotalSerializer(serializers.Serializer):
    total = serializers.DictField()
