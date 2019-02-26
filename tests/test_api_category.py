from django.test import TestCase

from rest_framework.test import APIClient

from money.models import Category


class CategoryAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_category(self):
        _category = {"name": "foo"}
        response = self.client.post('http://localhost:8000/api/money/category/', _category)
        self.assertEqual(response.status_code, 201)

    def test_create_category_name_missing(self):
        _category = {}
        response = self.client.post('http://localhost:8000/api/money/category/', _category)
        self.assertEqual(response.status_code, 400)

    def test_create_subcategory(self):
        _category = Category(name='foo')
        _category.save()

        _subcategory = {"name": "bar1",
                        'category': 'foo'}
        response = self.client.post('http://localhost:8000/api/money/subcategory/', _subcategory)
        self.assertEqual(response.status_code, 201)

        response = self.client.get('http://localhost:8000/api/money/category/')
        self.assertEqual(len(response.data[0]['subcategories']), 1)
