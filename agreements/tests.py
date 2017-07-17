from django.test import TestCase
from agreements.models import Agreement, AgreementText
from companies.models import Company
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import Group, ContentType, Permission

# Create your tests here.


class AgreementTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(company_name='Testbedrijf', company_address='Testadres',
                                              company_city_and_zipcode='Testplaats 1234AB')
        self.text = AgreementText.objects.create(title='Model',
                                                 text='TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST',
                                                 edited_at=timezone.now())
        self.agreement = Agreement.objects.create(agree_text=self.text, client_name='test',
                                                  client_emailaddress='test@test.nl',
                                                  company=self.company,
                                                  agreement_text_copy='TEST TEST TEST TEST',
                                                  created=timezone.now(), url='23556')
        self.user = User.objects.create_user(username='testuser', email='test@test.nl', password='secret')

        agreements_group = Group.objects.create(name='Overeenkomsttekst')
        content_type = ContentType.objects.get(model='agreementtext')
        all_permissions = Permission.objects.filter(content_type=content_type)
        agreements_group.permissions.set(all_permissions)
        agreements_group.save()

        self.user.groups.add(agreements_group)

        self.user.save()
        self.c = Client()

    def test_redirect_index_model_agreements(self):
        response = self.c.get(reverse('index_model_agreements'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_index_model_agreements(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('index_model_agreements'))
        self.assertTrue(self.text.title in response.context['model_agreements'].rows[0].get_cell(0))
        self.assertIsNotNone(response.context['model_agreements'].rows)

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
