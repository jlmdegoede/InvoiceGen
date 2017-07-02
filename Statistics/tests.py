from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import datetime
from HourRegistration.models import *
from django.utils import timezone
from Statistics.views import get_total_hours
from datetime import timedelta
# Create your tests here.


class StatisticsTestClass(TestCase):
    def setUp(self):
        now = timezone.now()
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

    def test_normal_hr(self):
        now = timezone.now()
        self.hr = HourRegistration.objects.create(start=now, end=now + timedelta(days=2), product=self.order_two)
        total_hours = get_total_hours(now.year)
        self.assertEqual(total_hours, 48)

    def test_normal_hr_multiple_uneven(self):
        now = timezone.now()
        self.hr = HourRegistration.objects.create(start=now, end=now + timedelta(days=2), product=self.order_two)
        self.hr = HourRegistration.objects.create(start=now + timedelta(days=3), end=now + timedelta(days=5), product=self.order_two)
        self.hr = HourRegistration.objects.create(start=now + timedelta(days=6), end=now + timedelta(days=8), product=self.order_two)
        total_hours = get_total_hours(now.year)
        self.assertEqual(total_hours, 144)

    def test_normal_hr_multiple_even(self):
        now = timezone.now()
        self.hr = HourRegistration.objects.create(start=now, end=now + timedelta(days=2), product=self.order_two)
        self.hr = HourRegistration.objects.create(start=now + timedelta(days=3), end=now + timedelta(days=5), product=self.order_two)
        self.hr = HourRegistration.objects.create(start=now + timedelta(days=6), end=now + timedelta(days=8), product=self.order_two)
        self.hr = HourRegistration.objects.create(start=now + timedelta(days=9), end=now + timedelta(days=15), product=self.order_two)
        total_hours = get_total_hours(now.year)
        self.assertEqual(total_hours, 288)

    def test_hr_without_end(self):
        now = timezone.now()
        self.hr = HourRegistration.objects.create(start=now - timedelta(days=1), end=None, product=self.order_two)
        total_hours = get_total_hours(now.year)
        self.assertEqual(total_hours, 24)

    def test_hr_same_time(self):
        now = timezone.now()
        self.hr = HourRegistration.objects.create(start=now, end=now, product=self.order_one)
        total_hours = get_total_hours(now.year)
        self.assertEqual(total_hours, 0)

    def test_hr_end_before_start(self):
        now = timezone.now()
        self.hr = HourRegistration.objects.create(start=now, end=now - timedelta(days=1), product=self.order_one)
        total_hours = get_total_hours(now.year)
        self.assertEqual(total_hours, 0)

    def test_hr_on_same_time(self):
        now = timezone.now()
        self.hr_one = HourRegistration.objects.create(start=now - timedelta(days=1), end=now, product=self.order_one)
        self.hr_two = HourRegistration.objects.create(start=now - timedelta(days=1), end=now, product=self.order_two)
        total_hours = get_total_hours(now.year)
        self.assertEqual(total_hours, 24)

    def test_hr_on_same_time_different_start(self):
        now = timezone.now()
        self.hr_one = HourRegistration.objects.create(start=now - timedelta(days=2), end=now, product=self.order_one)
        self.hr_two = HourRegistration.objects.create(start=now - timedelta(days=1), end=now, product=self.order_two)
        total_hours = get_total_hours(now.year)
        self.assertEqual(total_hours, 48)

    def test_hr_on_same_time_different_end(self):
        now = timezone.now()
        self.hr_one = HourRegistration.objects.create(start=now - timedelta(days=1), end=now + timedelta(days=1), product=self.order_one)
        self.hr_two = HourRegistration.objects.create(start=now - timedelta(days=1), end=now, product=self.order_two)
        total_hours = get_total_hours(now.year)
        self.assertEqual(total_hours, 48)

    def test_hr_on_same_time_different_start_and_end(self):
        now = timezone.now()
        self.hr_one = HourRegistration.objects.create(start=now - timedelta(days=1), end=now + timedelta(days=4), product=self.order_one)
        self.hr_two = HourRegistration.objects.create(start=now - timedelta(days=3), end=now + timedelta(days=1), product=self.order_two)
        total_hours = get_total_hours(now.year)
        self.assertEqual(total_hours, 168)

