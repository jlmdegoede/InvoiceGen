from django.test import TestCase
import datetime
from django.test import Client
from django.contrib.auth.models import User
from .models import *
from django.core.urlresolvers import reverse
from Settings.models import UserSetting
from HourRegistration.models import *

class OrderTestCase(TestCase):
    def setUp(self):
        now = datetime.datetime.now()
        next_week = now + datetime.timedelta(7)
        self.company = Company.objects.create(company_name='Testbedrijf', company_address='Testadres',
                                              company_city_and_zipcode='Testplaats 1234AB')
        self.order_one = Product.objects.create(title='Testopdracht 1', date_received=now, date_deadline=next_week, quantity=1000,
                             from_company=self.company, identification_number=1, briefing='Test',
                             price_per_quantity=0.25, tax_rate=21)
        self.order_two = Product.objects.create(title='Testopdracht 2', date_received=now, date_deadline=next_week, quantity=700,
                             from_company=self.company, identification_number=1, briefing='Test',
                             price_per_quantity=0.22, tax_rate=0)
        self.c = Client()
        self.user = User.objects.create_user(username='testuser', email='test@test.nl', password='secret')


    def test_index(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('index'))
        self.assertTrue(self.order_one.title in response.context['active_products_table'].rows[0].get_cell(1))
        self.assertTrue(self.order_two.title in response.context['active_products_table'].rows[1].get_cell(1))


    def test_no_settings_notification(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('index'))
        self.assertTrue(response.context['first_time'])
        user_setting = UserSetting.objects.create(name='Testnaam', address='Testadres',
                                                       city_and_zipcode='Teststad 1234AB', email='test@test.test',
                                                       iban='NL000BANK')
        response = self.c.get(reverse('index'))
        self.assertFalse(response.context['first_time'])

    def test_view_product(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('view_product', args=(self.order_one.id, self.order_one.title)))
        self.assertEqual(self.order_one, response.context['product'])

    def test_view_product_with_hour_registration(self):
        self.c.login(username='testuser', password='secret')
        now = datetime.datetime.now()
        next_hour = datetime.datetime.now() + datetime.timedelta(0,60*60)
        hour_registration = HourRegistration.objects.create(start=now, end=next_hour, product=self.order_one)
        response = self.c.get(reverse('view_product', args=(self.order_one.id, self.order_one.title)))
        self.assertEqual(response.context['total_hours'], 1)
        self.assertTrue(hour_registration in response.context['hourregistrations'])

    def test_view_product_with_hour_registration_no_end(self):
        self.c.login(username='testuser', password='secret')
        now = datetime.datetime.now()
        hour_registration = HourRegistration.objects.create(start=now, product=self.order_one)
        response = self.c.get(reverse('view_product', args=(self.order_one.id, self.order_one.title)))
        self.assertEqual(response.context['total_hours'], 0)
        self.assertTrue(hour_registration in response.context['hourregistrations'])

    def test_index_logged_in(self):
        response = self.c.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)
