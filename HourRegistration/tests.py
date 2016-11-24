from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime
from Orders.models import *
from .models import *
from django.utils import timezone

# Create your tests here.


class HourRegistrationTestClass(TestCase):
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

    def test_start_time_tracking_login(self):
        response = self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_start_time_tracking(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        self.assertEqual(response.status_code, 200)
        str(response.content, encoding='utf8')
        self.assertContains(response, 'success')

    def test_start_time_tracking_existing(self):
        self.c.login(username='testuser', password='secret')
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        response = self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        self.assertEqual(response.status_code, 200)
        response_str = str(response.content, encoding='utf8')
        self.assertTrue(str(self.order_one.id) in response_str)
        self.assertContains(response, 'pk')
        self.assertContains(response, self.order_one.title)

    def test_end_time_tracking(self):
        self.c.login(username='testuser', password='secret')
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        response_end = self.c.get(reverse('end_time_tracking', kwargs={'product_id': self.order_one.id}))
        self.assertContains(response_end, 'success')
        hour_registration = HourRegistration.objects.filter(product=self.order_one, end=None)
        self.assertTrue(hour_registration.count() == 0)

    def test_end_time_tracking_login(self):
        response = self.c.get(reverse('end_time_tracking', kwargs={'product_id': self.order_one.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_add_description_to_hourregistration(self):
        self.c.login(username='testuser', password='secret')
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        test_description = 'Testomschrijving'
        response = self.c.post(reverse('add_description_to_hourregistration'), data={'description': test_description, 'product_id': self.order_one.id})
        self.assertContains(response, 'success')
        h_registration = HourRegistration.objects.filter(product=self.order_one, end=None, description=test_description)
        self.assertTrue(h_registration.count() != 0)

    def test_get_description_to_hourregistration(self):
        self.c.login(username='testuser', password='secret')
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        test_description = 'Testomschrijving'
        self.c.post(reverse('add_description_to_hourregistration'), data={'description': test_description, 'product_id': self.order_one.id})
        response_get = self.c.get(reverse('add_description_to_hourregistration'), data={'product_id': self.order_one.id})
        self.assertContains(response_get, test_description)

    def test_get_description_multiple_hrs(self):
        self.c.login(username='testuser', password='secret')
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        self.c.get(reverse('end_time_tracking', kwargs={'product_id': self.order_one.id}))
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        self.c.get(reverse('end_time_tracking', kwargs={'product_id': self.order_one.id}))
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        test_description = 'Testomschrijving'
        self.c.post(reverse('add_description_to_hourregistration'), data={'description': test_description, 'product_id': self.order_one.id})
        response = self.c.get(reverse('add_description_to_hourregistration'), data={'product_id': self.order_one.id})
        self.assertContains(response, test_description)

    def test_add_description_to_hourregistration_login(self):
        response = self.c.post(reverse('add_description_to_hourregistration'), data={'description': 'Testomschrijving', 'product_id': self.order_one.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_existing_time_tracking(self):
        self.c.login(username='testuser', password='secret')
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        response = self.c.get(reverse('existing_time_tracking'))
        response_str = str(response.content, encoding='utf8')
        self.assertTrue(str(self.order_one.id) in response_str)
        self.assertContains(response, 'pk')
        self.assertContains(response, self.order_one.title)

    def test_multiple_existing_time_tracking(self):
        self.c.login(username='testuser', password='secret')
        # order is important
        # existing is expected to return the first one started
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_two.id}))
        response = self.c.get(reverse('existing_time_tracking'))
        response_str = str(response.content, encoding='utf8')
        self.assertTrue(str(self.order_one.id) in response_str)
        self.assertContains(response, 'pk')
        self.assertContains(response, self.order_one.title)

    def test_none_existing_time_tracking(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('existing_time_tracking'))
        self.assertContains(response, 'existing')
        self.assertContains(response, 'False')

    def test_existing_time_tracking_login(self):
        response = self.c.get(reverse('existing_time_tracking'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_delete_hourregistration(self):
        self.c.login(username='testuser', password='secret')
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        response = self.c.post(reverse('delete_time_tracking'), data={'time_id': 1})
        self.assertContains(response, 'success')
        self.assertContains(response, 'true')
        h_registration = HourRegistration.objects.filter(id=1)
        self.assertEqual(h_registration.count(), 0)

    def test_delete_hourregistration_non_existing(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.post(reverse('delete_time_tracking'), data={'time_id': 1})
        self.assertContains(response, 'error')

    def test_delete_hourregistration_login(self):
        response = self.c.post(reverse('delete_time_tracking'), data={'time_id': 1})
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_set_end_time(self):
        self.c.login(username='testuser', password='secret')
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        now = timezone.now()
        response = self.c.post(reverse('set_end_time'), data={'pk': 1, 'endDate': now.strftime('%d-%m-%Y'), 'endTime': now.strftime('%H:%M')})
        self.assertContains(response, 'success')
        self.assertContains(response, 'true')

    def test_set_end_time_missing_pk(self):
        self.c.login(username='testuser', password='secret')
        self.c.get(reverse('start_time_tracking', kwargs={'product_id': self.order_one.id}))
        now = timezone.now()
        response = self.c.post(reverse('set_end_time'), data={'endDate': now.strftime('%d-%m-%Y'), 'endTime': now.strftime('%H:%M')})
        self.assertContains(response, 'success')
        self.assertContains(response, 'false')

    def test_set_end_time_login(self):
        response = self.c.post(reverse('set_end_time'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_create_new_hour_registration(self):
        self.c.login(username='testuser', password='secret')
        now = timezone.now()

        data = dict()
        data['startDate'] = now.strftime('%d-%m-%Y')
        data['startTime'] = now.strftime('%H:%M')
        data['endDate'] =  now.strftime('%d-%m-%Y')
        data['endTime'] = now.strftime('%H:%M')
        data['product_id'] = self.order_one.id

        response = self.c.post(reverse('create_new_hour_registration'), data=data)
        self.assertContains(response, 'success')
        self.assertContains(response, 'true')

    def test_create_new_hour_registration_login(self):
        response = self.c.post(reverse('create_new_hour_registration'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)
