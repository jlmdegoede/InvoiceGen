from Companies.models import Company
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from Orders.models import Product
from django.utils import timezone
from django.contrib.auth.models import Group, ContentType, Permission
# Create your tests here.


class CompaniesTestCase(TestCase):

    def setUp(self):
        self.first_company = Company.objects.create(company_name='Testbedrijf', company_address='Testadres',
                                              company_city_and_zipcode='Testplaats 1234AB', company_email='test@test.test')
        self.first_product = Product.objects.create(title='Testopdracht', date_deadline=timezone.now(), date_received=timezone.now(), quantity=500, from_company=self.first_company,
                                     identification_number=0, price_per_quantity=0.25, tax_rate=0)
        self.c = Client()

        group = Group.objects.create(name='Bedrijven')
        content_type = ContentType.objects.get(model='company')
        all_permissions = Permission.objects.filter(content_type=content_type)
        group.permissions.set(all_permissions)
        group.save()

        self.user = User.objects.create_user(username='testuser', email='test@test.nl', password='secret')
        self.user.groups.add(group)
        self.user.save()

    def test_index(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('company_index'))
        self.assertEqual(response.context['companies'][0].company_name, self.first_company.company_name)

    def test_index_login(self):
        response = self.c.get(reverse('company_index'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login' in response.url)

    def test_delete_company_not_logged_in(self):
        response = self.c.get(reverse('company_delete', kwargs={'company_id': self.first_company.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login' in response.url)

    def test_edit_company_not_logged_in(self):
        response = self.c.get(reverse('company_edit', kwargs={'company_id': self.first_company.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login' in response.url)

    def test_add_company_not_logged_in(self):
        response = self.c.get(reverse('company_add'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login' in response.url)

    def test_delete_company_with_product(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('company_delete', kwargs={'company_id': self.first_company.id}))
        self.assertIsNotNone(self.first_company)

    def test_delete_non_existing_company(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('company_delete', kwargs={'company_id': 232323}))
        self.assertEqual(self.c.session['toast'], 'Opdrachtgever niet verwijderd')

    def test_delete_existing_company(self):
        self.first_product.delete()
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('company_delete', kwargs={'company_id': self.first_company.id}))
        self.assertEqual(Company.objects.filter(id=self.first_company.id).count(), 0)
        self.assertEqual(self.c.session['toast'], 'Opdrachtgever verwijderd')

    def test_add_company_form(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('company_add'))
        self.assertIsNotNone(response.context['form'])

    def test_add_post_company_form(self):
        self.c.login(username='testuser', password='secret')
        data = {'company_name': 'TEST', 'company_address': 'Test Test Test',
                'company_city_and_zipcode': 'Test Test Test', 'company_email': 'test@test.test'}
        response_post = self.c.post(reverse('company_add'), data)
        response_index = self.c.get(reverse('company_index'))
        self.assertEqual(response_index.context['companies'].count(), 2)

    def test_add_post_missing_cityzipcode_company_form(self):
        self.c.login(username='testuser', password='secret')
        data = {'company_name': 'TEST', 'company_address': 'Test Test Test',
                'company_email': 'test@test.test'}
        response_post = self.c.post(reverse('company_add'), data)
        response_index = self.c.get(reverse('company_index'))
        self.assertEqual(response_index.context['companies'].count(), 1)
        self.assertIsNotNone(response_post.context['error'])

    def test_add_post_missing_name_company_form(self):
        self.c.login(username='testuser', password='secret')
        data = {'company_address': 'Test Test Test', 'company_city_and_zipcode': 'Test Test Test',
                'company_email': 'test@test.test'}
        response_post = self.c.post(reverse('company_add'), data)
        response_index = self.c.get(reverse('company_index'))
        self.assertEqual(response_index.context['companies'].count(), 1)
        self.assertIsNotNone(response_post.context['error'])

    def test_add_post_missing_address_company_form(self):
        self.c.login(username='testuser', password='secret')
        data = {'company_address': 'Test Test Test', 'company_city_and_zipcode': 'Test Test Test'}
        response_post = self.c.post(reverse('company_add'), data)
        response_index = self.c.get(reverse('company_index'))
        self.assertEqual(response_index.context['companies'].count(), 1)
        self.assertIsNotNone(response_post.context['error'])

    def test_edit_get_company(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('company_edit', kwargs={'company_id': self.first_company.id}))
        self.assertEqual(response.context['company_id'], self.first_company.id)
        self.assertIsNotNone(response.context['form'])

    def test_edit_get_non_existing_company(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('company_edit', kwargs={'company_id': 232323}))
        self.assertEqual(response.status_code, 302)

    def test_edit_company(self):
        self.c.login(username='testuser', password='secret')
        data = {'company_name': 'Testcase', 'company_address': 'TESTCASE1', 'company_city_and_zipcode': 'Test Test Test', 'company_email': 'test@test.test'}
        response_post = self.c.post(reverse('company_edit', kwargs={'company_id': self.first_company.id}), data)
        response_index = self.c.get(reverse('company_index'))
        self.assertEqual(response_index.context['companies'][0].company_name, data['company_name'])

    def test_edit_company_invalid(self):
        self.c.login(username='testuser', password='secret')
        data = {'company_name': 'Testcase', 'company_address': 'TESTCASE1',}
        response = self.c.post(reverse('company_edit', kwargs={'company_id': self.first_company.id}), data)
        self.assertEqual(response.context['company_id'], self.first_company.id)
        self.assertIsNotNone(response.context['form'])
        self.assertIsNotNone(response.context['error'])
