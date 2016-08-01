from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime
from Orders.models import *
from .models import *

# Create your tests here.


class HourRegistrationTestClass(TestCase):
    def setUp(self):
        now = datetime.datetime.now()
        next_week = now + datetime.timedelta(7)
        self.company = Company.objects.create(company_name='Testbedrijf', company_address='Testadres',
                                              company_city_and_zipcode='Testplaats 1234AB')
        self.order_one = Product.objects.create(title='Testopdracht 1', date_received=now, date_deadline=next_week,
                                                quantity=1000,
                                                from_company=self.company, identification_number=1, briefing='Test',
                                                price_per_quantity=0.25, tax_rate=21)
        self.order_two = Product.objects.create(title='Testopdracht 2', date_received=now, date_deadline=next_week,
                                                quantity=700,
                                                from_company=self.company, identification_number=1, briefing='Test',
                                                price_per_quantity=0.22, tax_rate=0)
        self.c = Client()
        self.user = User.objects.create_user(username='testuser', email='test@test.nl', password='secret')

    def test_start_time_tracking(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('index', kwargs={'product_id': self.order_one.id}))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': 'True'}
        )