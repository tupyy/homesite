# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate,requests
from django.core.urlresolvers import reverse
from rest_framework.test import APIRequestFactory,APIClient
from views import *

class TestSerializers(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user('testuser',password='testing')
        self.user.save()

    def test_categories(self):

        self.client = APIClient()
        self.response = self.client.get('http://127.0.0.1:8000/api/subcategory',format='json')
        assert self.response.status_code == 200
