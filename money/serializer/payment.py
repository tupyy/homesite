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
    comments = serializers.CharField(required=False)

    def create(self, validated_data):
        if self.is_valid(raise_exception=True):
            _category = Category.objects.get(name=self.validated_data['category'])
            _subcategory = Subcategory.objects.filter(name=self.validated_data['subcategory'],
                                                      category__name=_category.name).first()
            _user = User.objects.get(username=self.validated_data['user'])
            _payment = Payment.objects.create(user=_user,
                                              category=_category,
                                              subcategory=_subcategory,
                                              sum=float(validated_data['sum']),
                                              date=validated_data['date'],
                                              comments=validated_data.get('comments', ''))
            return _payment

    def update(self, instance, validated_data):
        if self.is_valid(raise_exception=True):
            _category = Category.objects.get(name=self.validated_data['category'])
            _subcategory = Subcategory.objects.filter(name=self.validated_data['subcategory'],
                                                      category__name=_category.name).first()
            _user = User.objects.get(username=self.validated_data['user'])

            instance.category = _category
            instance.user = _user
            instance.subcategory = _subcategory
            instance.sum = validated_data.get("sum", instance.sum)
            instance.date = validated_data.get('date', instance.date)
            instance.comments = validated_data.get('comments', instance.comments)
            instance.save()
            return instance

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
            raise ValidationError(
                'Subcategory {} is not part of category {}'.format(value, self.initial_data['category']))
        return value

    def validate_user(self, value):
        try:
            _user = get_object_or_404(User, username=self.initial_data['user'])
            return value
        except Http404:
            raise ValidationError('User {} do not exists.'.format(self.initial_data['user']))


class TotalSerializer(serializers.Serializer):
    total = serializers.DictField()
