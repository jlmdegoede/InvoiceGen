from django.test import TestCase
import datetime
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from Settings.models import UserSetting
from HourRegistration.models import *


class OrderTestCase(TestCase):
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

    def test_index(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('index'))
        self.assertTrue(self.order_one.title in response.context['active_products_table'].rows[0].get_cell(1))
        self.assertTrue(self.order_two.title in response.context['active_products_table'].rows[1].get_cell(1))

    def test_index_not_logged_in(self):
        response = self.c.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

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
        next_hour = datetime.datetime.now() + datetime.timedelta(0, 60 * 60)
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

    def test_view_product_not_logged_in(self):
        response = self.c.get(reverse('view_product', args=(self.order_one.id, self.order_one.title)))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_mark_products_as_done(self):
        self.c.login(username='testuser', password='secret')
        data = {'products[]': [1, 2]}
        response = self.c.post(reverse('mark_products_as_done'), data)
        product_one_fresh = Product.objects.get(pk=1)
        product_two_fresh = Product.objects.get(pk=2)
        self.assertEqual(product_one_fresh.done, True)
        self.assertEqual(product_two_fresh.done, True)

    def test_mark_products_as_done_empty(self):
        self.c.login(username='testuser', password='secret')
        data = {'products[]': []}
        response = self.c.post(reverse('mark_products_as_done'), data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True}
        )

    def test_mark_products_as_done_not_logged_in(self):
        data = {'products[]': []}
        response = self.c.post(reverse('mark_products_as_done'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_add_company_inline_post(self):
        self.c.login(username='testuser', password='secret')
        data = {'company_name': 'Testcase', 'company_address': 'TESTCASE1',
                'company_city_and_zipcode': 'Test Test Test'}
        response = self.c.post(reverse('add_company_inline'), data)
        new_company = Company.objects.get(pk=2)
        self.assertIsNotNone(new_company)
        self.assertEqual(new_company.company_name, 'Testcase')

    def test_add_company_inline_get(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('add_company_inline'))
        self.assertIsNotNone(response.context['form'])

    def test_add_company_inline_get_not_logged_in(self):
        response = self.c.get(reverse('add_company_inline'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_add_product_get(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('add_product'))
        self.assertIsNotNone(response.context['form'])

    def test_add_product_get_not_logged_in(self):
        response = self.c.get(reverse('add_product'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_add_product_post(self):
        self.c.login(username='testuser', password='secret')
        now = datetime.datetime.now().strftime('%d-%m-%Y')
        data = {'title': 'O1', 'date_received': now, 'date_deadline': now,
                'quantity': 500, 'briefing': '', 'price_per_quantity': 0.25, 'tax_rate': 21,
                'from_company': self.company.id, 'identification_number': 42}
        response = self.c.post(reverse('add_product'), data)
        new_product = Product.objects.get(title='O1')
        self.assertIsNotNone(new_product)

    def test_add_product_post_error(self):
        self.c.login(username='testuser', password='secret')
        now = datetime.datetime.now().strftime('%d-%m-%Y')
        data = {'title': 'O1', 'date_received': now, 'date_deadline': now,
                'quantity': 500, 'briefing': '',  'tax_rate': 21,
                'from_company': self.company.id, 'identification_number': 42}
        response = self.c.post(reverse('add_product'), data)
        self.assertIsNotNone(response.context['error'])

    def test_edit_product_get(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('edit_product', kwargs={'product_id': 1}))
        self.assertIsNotNone(response.context['form'])
        self.assertTrue(response.context['edit'])

    def test_edit_product_not_logged_in_get(self):
        response = self.c.get(reverse('edit_product', kwargs={'product_id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_edit_product_not_logged_in_post(self):
        response = self.c.post(reverse('edit_product', kwargs={'product_id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_edit_product_get_not_existent(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('edit_product', kwargs={'product_id': 999}))
        self.assertEqual(self.c.session['toast'], 'Opdracht niet gevonden')

    def test_edit_product_post(self):
        self.c.login(username='testuser', password='secret')
        now = datetime.datetime.now().strftime('%d-%m-%Y')
        data = {'title': 'O2', 'date_received': now, 'date_deadline': now,
                'quantity': 500, 'briefing': '', 'price_per_quantity': 0.25, 'tax_rate': 21,
                'from_company': self.company.id, 'identification_number': 42}
        response = self.c.post(reverse('edit_product', kwargs={'product_id': 1}), data)
        self.assertEqual(self.c.session['toast'], 'Opdracht gewijzigd')

    def test_edit_product_post_invalid(self):
        self.c.login(username='testuser', password='secret')
        now = datetime.datetime.now().strftime('%d-%m-%Y')
        data = {'date_received': now, 'date_deadline': now,
                'quantity': 500, 'briefing': '', 'price_per_quantity': 0.25, 'tax_rate': 21,
                'from_company': self.company.id, 'identification_number': 42}
        response = self.c.post(reverse('edit_product', kwargs={'product_id': 1}), data)
        self.assertEqual(response.context['toast'], 'Ongeldig formulier')
        self.assertIsNotNone(response.context['form'])
        self.assertTrue(response.context['edit'])

    def test_delete_product(self):
        self.c.login(username='testuser', password='secret')
        self.assertIsNotNone(Product.objects.get(pk=1))
        response = self.c.get(reverse('delete_product', kwargs={'product_id': 1}))
        self.assertEqual(self.c.session['toast'], 'Opdracht verwijderd')
        self.assertEqual(Product.objects.filter(pk=1).count(), 0)
        self.assertEqual(response.status_code, 302)

    def test_delete_product_invalid(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('delete_product', kwargs={'product_id': 999}))
        self.assertEqual(self.c.session['toast'], 'Verwijderen mislukt')

    def test_delete_product_not_logged_in(self):
        response = self.c.get(reverse('delete_product', kwargs={'product_id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_delete_product_not_logged_in_invalid_id(self):
        response = self.c.get(reverse('delete_product', kwargs={'product_id': 999}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)