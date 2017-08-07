from datetime import date, timedelta

from django.contrib.auth.models import ContentType, Group, Permission, User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.utils import timezone

from companies.models import Company
from orders.models import Product
from settings.models import UserSetting

from .models import OutgoingInvoice


class InvoicesTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(company_name='Testbedrijf', company_address='Testadres',
                                              company_city_and_zipcode='Testplaats 1234AB')

        self.invoice_current = OutgoingInvoice.objects.create(title='Factuur 1', date_created=timezone.now(),
                                                      to_company=self.company, invoice_number=1,
                                                      expiration_date=timezone.now() + timedelta(days=62))

        self.invoice_year_old = OutgoingInvoice.objects.create(title='Factuur 2', date_created=date(2015, 10, 1),
                                                       to_company=self.company, invoice_number=2,
                                                       expiration_date=date(2015, 11, 1))
        self.product = Product.objects.create(title='Testopdracht', date_deadline=timezone.now(),
                                                    date_received=timezone.now(), quantity=500,
                                                    from_company=self.company,
                                                    identification_number=0, price_per_quantity=0.25, tax_rate=0)
        self.user = User.objects.create_user(username='testuser', email='test@test.nl', password='secret')
        self.c = Client()
        group = Group.objects.create(name='Facturen')
        content_type = ContentType.objects.get(model='outgoinginvoice')
        all_permissions = Permission.objects.filter(content_type=content_type)
        group.permissions.set(all_permissions)
        group.save()
        self.user.groups.add(group)
        self.user.save()

        self.user_setting = UserSetting.objects.create(name='Testnaam', address='Testadres', city_and_zipcode='Teststad 1234AB', email='test@test.test', iban='NL000BANK')

    def test_get_invoices(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('get_invoices'))
        self.assertTrue(2015 in response.context['years'])
        self.assertTrue(timezone.now().year in response.context['years'])
        self.assertTrue(self.invoice_current.title in response.context['invoices'][timezone.now().year].rows[0].get_cell(1))
        self.assertTrue(self.invoice_year_old.title in response.context['invoices'][2015].rows[0].get_cell(1))

    def test_delete_valid_invoice(self):
        self.c.login(username='testuser', password='secret')
        self.c.get(reverse('delete_outgoing_invoice', kwargs={'invoiceid': self.invoice_current.id}))
        self.assertEqual(self.c.session['toast'], 'Verwijderen factuur gelukt')

    def test_delete_invalid_invoice(self):
        self.c.login(username='testuser', password='secret')
        self.c.get(reverse('delete_outgoing_invoice', kwargs={'invoiceid': 1212}))
        self.assertEqual(self.c.session['toast'], 'Verwijderen factuur mislukt')

    def test_creating_invoice_valid(self):
        self.c.login(username='testuser', password='secret')
        data = {'title': 'Factuur 1', 'invoice_number': 1, 'total_amount': 250,
                'expiration_date': timezone.now().strftime('%d-%m-%Y'), 'paid': False, 'products': [1]}
        response = self.c.post(reverse('add_outgoing_invoice'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('facturen' in response.url)
        response_index = self.c.get(reverse('get_invoices'))
        self.assertEqual(response_index.context['invoices'][timezone.now().year].paginator.count, 2)

    def test_generate_invoice(self):
        self.c.login(username='testuser', password='secret')
        data = {'products[]': [1], 'volgnummer': 2}
        self.c.post(reverse('generate_invoice'), data)
        invoice = OutgoingInvoice.objects.get(id=3)
        self.assertEqual(invoice.invoice_number, '2')

    def test_get_invoices_not_logged_in(self):
        response = self.c.get(reverse('get_invoices'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_add_invoice_not_logged_in(self):
        response = self.c.get(reverse('add_outgoing_invoice'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_edit_invoice_not_logged_in(self):
        response = self.c.get(reverse('edit_outgoing_invoice', kwargs={'invoiceid': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_delete_invoice_not_logged_in(self):
        response = self.c.get(reverse('delete_outgoing_invoice', kwargs={'invoiceid': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)
