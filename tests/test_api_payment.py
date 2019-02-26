from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from money.models import Category, Subcategory, Payment


class PaymentAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # create user
        _user = User(username='admin', password='foo')
        _user.save()

        # create one category with one subcategory
        _category = Category(name='alimente')
        _category.save()
        _subcategory = Subcategory(name='mancare',
                                   category=_category)
        _subcategory.save()

    def test_create_payment_nominal(self):
        _payment = {"user": "admin",
                    "category": "alimente",
                    "subcategory": "mancare",
                    "sum": 20,
                    "date": "2019-02-03",
                    "comments": "teste"
                    }
        response = self.client.post('http://localhost:8000/api/money/payment/', _payment)
        self.assertEqual(response.status_code, 201)

    def test_update_payment_nominal(self):
        _payment = {"user": "admin",
                    "category": "alimente",
                    "subcategory": "mancare",
                    "sum": 20,
                    "date": "2019-02-03",
                    "comments": "teste"
                    }
        response = self.client.post('http://localhost:8000/api/money/payment/', _payment)
        self.assertEqual(response.status_code, 201)

        _payment['sum'] = 40
        response = self.client.put('http://localhost:8000/api/money/payment/{}/'.format(response.data['id']), _payment)
        self.assertEqual(response.status_code, 200)

    def test_update_payment_400(self):
        _payment = {"user": "admin",
                    "category": "alimente",
                    "subcategory": "mancare",
                    "sum": 20,
                    "date": "2019-02-03",
                    "comments": "teste"
                    }
        response = self.client.post('http://localhost:8000/api/money/payment/', _payment)
        self.assertEqual(response.status_code, 201)

        _payment['sum'] = 40
        _payment['subcategory'] = 'bar'
        response = self.client.put('http://localhost:8000/api/money/payment/{}/'.format(response.data['id']), _payment)
        self.assertEqual(response.status_code, 400)

    def test_create_payment_no_category(self):
        _payment = {"user": "admin",
                    "category": "dont_exists",
                    "subcategory": "mancare",
                    "sum": 20,
                    "date": "2019-02-03",
                    "comments": "teste"
                    }
        response = self.client.post('http://localhost:8000/api/money/payment/', _payment)
        self.assertEqual(response.status_code, 400)

    def test_create_payment_no_subcategory(self):
        _payment = {"user": "admin",
                    "category": "alimente",
                    "subcategory": "foo",
                    "sum": 20,
                    "date": "2019-02-03",
                    "comments": "teste"
                    }
        response = self.client.post('http://localhost:8000/api/money/payment/', _payment)
        self.assertEqual(response.status_code, 400)

    def test_create_payment_category(self):
        """Category foo do not have subcategory bar"""
        _category = Category(name='foo')
        _category.save()

        _payment = {"user": "admin",
                    "category": "foo",
                    "subcategory": "mancare",
                    "sum": 20,
                    "date": "2019-02-03",
                    "comments": "teste"
                    }
        response = self.client.post('http://localhost:8000/api/money/payment/', _payment)
        self.assertEqual(response.status_code, 400)

    def test_get_payment(self):
        """Category foo do not have subcategory bar"""
        _payment = {"user": "admin",
                    "category": "alimente",
                    "subcategory": "mancare",
                    "sum": 20,
                    "date": "2019-02-03",
                    "comments": "teste"
                    }
        response = self.client.post('http://localhost:8000/api/money/payment/', _payment)
        self.assertEqual(response.status_code, 201)

        response = self.client.get('http://localhost:8000/api/money/payment/')
        self.assertEqual(len(response.data), 1)

    def test_filter_payments(self):
        self._create_payments()
        response = self.client.get('http://localhost:8000/api/money/payment/')
        self.assertEqual(len(response.data), 4)

    def test_filter_payments2(self):
        self._create_payments()
        response = self.client.get('http://localhost:8000/api/money/payment/?month=1')
        self.assertEqual(len(response.data), 2)

    def test_filter_payments3(self):
        self._create_payments()
        response = self.client.get('http://localhost:8000/api/money/payment/?year=2018')
        self.assertEqual(len(response.data), 0)

    def test_filter_payments4(self):
        self._create_payments()
        response = self.client.get('http://localhost:8000/api/money/payment/?start_date=2019-01-01&end_date=2019-01-31')
        self.assertEqual(len(response.data), 2)

    def test_filter_payments5(self):
        self._create_payments()
        response = self.client.get('http://localhost:8000/api/money/payment/?category=cat1')

        # 2 payments for cat1
        self.assertEqual(len(response.data), 2)

    def test_filter_payments6(self):
        self._create_payments()
        response = self.client.get('http://localhost:8000/api/money/payment/?category=cat1&month=1')
        self.assertEqual(len(response.data), 1)

    def test_filter_payments7(self):
        self._create_payments()
        response = self.client.get('http://localhost:8000/api/money/payment/?category=cat2&month=1')
        self.assertEqual(len(response.data), 1)

    def test_filter_payments8(self):
        self._create_payments()
        response = self.client.get('http://localhost:8000/api/money/payment/?category=cat2&subcategory=sub_cat2')
        self.assertEqual(len(response.data), 2)

    def test_filter_payments9(self):
        self._create_payments()
        response = self.client.get('http://localhost:8000/api/money/payment/?category=cat2&subcategory=foo')
        self.assertEqual(len(response.data), 0)

    def _create_payments(self):
        category_names = ['cat1', 'cat2']
        categories = []
        for c in category_names:
            _category = Category(name=c)
            _category.save()
            _subcategory = Subcategory(name='sub_' + _category.name,
                                       category=_category)
            _subcategory.save()
            categories.append((_category, _subcategory))

        dates = ['2019-01-01', '2019-02-01']
        for cat, subcat in categories:
            for d in dates:
                _payment = Payment(category=cat,
                                   subcategory=subcat,
                                   sum=10,
                                   date=datetime.strptime(d, '%Y-%m-%d'))
                _payment.save()
