from django.test import TestCase
from Agreements.models import Agreement, AgreementText
from Companies.models import Company
from datetime import datetime, timedelta, date
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .models import Invoice
from Settings.models import UserSetting
from Orders.models import Product
from datetime import datetime
# Create your tests here.


class InvoicesTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(company_name='Testbedrijf', company_address='Testadres',
                                              company_city_and_zipcode='Testplaats 1234AB')

        self.invoice_current = Invoice.objects.create(title='Factuur 1', date_created=datetime.now(),
                                                      to_company=self.company, invoice_number=1, total_amount=250,
                                                      expiration_date=datetime.now() + timedelta(days=62))

        self.invoice_year_old = Invoice.objects.create(title='Factuur 2', date_created=date(2015, 10, 1),
                                                       to_company=self.company, invoice_number=2, total_amount=250,
                                                       expiration_date=date(2015, 11, 1))
        self.product = Product.objects.create(title='Testopdracht', date_deadline=datetime.now(),
                                                    date_received=datetime.now(), quantity=500,
                                                    from_company=self.company,
                                                    identification_number=0, price_per_quantity=0.25, tax_rate=0)
        self.user = User.objects.create_user(username='testuser', email='test@test.nl', password='secret')
        self.user_setting = UserSetting.objects.create(name='Testnaam', address='Testadres', city_and_zipcode='Teststad 1234AB', email='test@test.test', iban='NL000BANK')
        self.c = Client()

    def test_get_invoices(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('get_invoices'))
        self.assertTrue(2015 in response.context['years'])
        self.assertTrue(datetime.now().year in response.context['years'])
        self.assertTrue(self.invoice_current in response.context['invoices'][datetime.now().year])
        self.assertTrue(self.invoice_year_old in response.context['invoices'][2015])

    def test_delete_valid_invoice(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('delete_invoice', kwargs={'invoiceid': self.invoice_current.id}))
        self.assertEqual(self.c.session['toast'], 'Verwijderen factuur gelukt')

    def test_delete_invalid_invoice(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('delete_invoice', kwargs={'invoiceid': 1212}))
        self.assertEqual(self.c.session['toast'], 'Verwijderen factuur mislukt')

    def test_creating_invoice_valid(self):
        self.c.login(username='testuser', password='secret')
        data = {'title': 'Factuur 1', 'invoice_number': 1, 'total_amount': 250,
                'expiration_date': datetime.now().strftime('%d-%m-%Y'), 'paid': False, 'articles': [1]}
        response = self.c.post(reverse('add_invoice'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('facturen' in response.url)
        response_index = self.c.get(reverse('get_invoices'))
        self.assertEqual(response_index.context['invoices'][datetime.now().year].count(), 2)

    def test_creating_invoice_markdown(self):
        self.c.login(username='testuser', password='secret')
        data = {'title': 'Factuur 1', 'invoice_number': 1, 'total_amount': 250,
                'expiration_date': datetime.now().strftime('%d-%m-%Y'), 'paid': False, 'articles': [1]}
        response = self.c.post(reverse('add_invoice'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('facturen' in response.url)
        invoice = Invoice.objects.get(id=3)
        self.assertTrue('Testbedrijf' in invoice.contents)
        self.assertTrue('Testnaam' in invoice.contents)
        self.assertTrue(invoice.title in invoice.contents)

    def test_generate_invoice(self):
        self.c.login(username='testuser', password='secret')
        data = {'articles[]': [1], 'volgnummer': 2}
        response = self.c.post(reverse('generate_invoice'), data)
        self.assertEqual(response.status_code, 302)
        invoice = Invoice.objects.get(id=3)
        self.assertTrue(self.product.title in invoice.contents)

    def test_get_invoices_not_logged_in(self):
        response = self.c.get(reverse('get_invoices'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_add_invoice_not_logged_in(self):
        response = self.c.get(reverse('add_invoice'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_edit_invoice_not_logged_in(self):
        response = self.c.get(reverse('edit_invoice', kwargs={'invoiceid': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_delete_invoice_not_logged_in(self):
        response = self.c.get(reverse('delete_invoice', kwargs={'invoiceid': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)
