from django.test import TestCase
from Agreements.models import Agreement, AgreementText
from Companies.models import Company
import datetime
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your tests here.


class AgreementTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(company_name='Testbedrijf', company_address='Testadres',
                                              company_city_and_zipcode='Testplaats 1234AB')
        self.text = AgreementText.objects.create(title='Model',
                                                 text='TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST',
                                                 edited_at=datetime.datetime.now())
        self.agreement = Agreement.objects.create(agree_text=self.text, client_name='test',
                                                  client_emailaddress='test@test.nl',
                                                  company=self.company,
                                                  agreement_text_copy='TEST TEST TEST TEST',
                                                  created=datetime.datetime.now(), url='23556')
        self.user = User.objects.create_user(username='testuser', email='test@test.nl', password='secret')
        self.c = Client()

    def test_redirect_index_model_agreements(self):
        response = self.c.get(reverse('index_model_agreements'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_index_model_agreements(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('index_model_agreements'))
        self.assertEqual(response.context['model_agreements'][0].title, self.text.title)

    def test_view_agreement(self):
        response = self.c.get(reverse('view_agreement', args=[self.agreement.url]))
        self.assertEqual(response.context['agreement'], self.agreement)

    def test_add_get_agreement_text(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('add_agreement_text'))
        self.assertIsNotNone(response.context['form'])

    def test_add_post_agreement_text(self):
        self.c.login(username='testuser', password='secret')
        data = {'title': 'TEST', 'text': 'Test Test Test'}
        response = self.c.post(reverse('add_agreement_text'), data)
        self.assertIsNone(response.context)

    def test_add_post_no_title_agreement_text(self):
        self.c.login(username='testuser', password='secret')
        data = {'text': 'Test Test Test'}
        response = self.c.post(reverse('add_agreement_text'), data)
        self.assertIsNotNone(response.context['error'])

    def test_add_post_no_text_agreement_text(self):
        self.c.login(username='testuser', password='secret')
        data = {'title': 'TEST'}
        response = self.c.post(reverse('add_agreement_text'), data)
        self.assertIsNotNone(response.context['error'])
