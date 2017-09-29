# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from models import *

class PaymentModelTests(APITestCase):

    def setUp(self):
        user = User.objects.create(username='cosmin')
        category = Category.objects.create(name='Alimente')
        subcategory = Subcategory.objects.create(name='Mancare',category=category)
        PaymentOption.objects.create(name='Tickete')

    def test_create_payment(self):
        """
        Ensure that the models are created and updated
        correctly
        """
        data = {
            "date": "2017-09-17",
            "sum": "33.00",
            "nb_option": "0",
            "comments": "commentary",
            "user": 1,
            "category": 1,
            "subcategory": 1,
            "option_pay": 1
        }

        response = self.client.post("/payment/",data,format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PaymentModel.objects.count(), 1)

    def test_get_payment(self):
        response = self.client.get('/payment/1/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def update_payment(self):
        data = {
            "date": "2017-09-17",
            "sum": "200.00",
            "nb_option": "0",
            "comments": "commentary",
            "user": 1,
            "category": 1,
            "subcategory": 1,
            "option_pay": 1
        }

        response = self.client.put("/payment/1/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PaymentModel.objects.count(), 1)

