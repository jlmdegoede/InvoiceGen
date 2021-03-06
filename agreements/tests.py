from django.contrib.auth.models import ContentType, Group, Permission, User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.utils import timezone

from agreements.models import Agreement, AgreementText
from companies.models import Company


class AgreementTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(company_name='Testbedrijf', company_address='Testadres',
                                              company_city_and_zipcode='Testplaats 1234AB')
        self.text = AgreementText.objects.create(title='Model',
                                                 text='Dit is een testtekstt',
                                                 edited_at=timezone.now())
        self.agreement = Agreement.objects.create(agreement_text=self.text, client_name='test',
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

    def test_redirect_agreementtext_index(self):
        response = self.c.get(reverse('agreementtext_index'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/accounts/login/?next=/' in response.url)

    def test_agreementtext_index(self):
        self.c.login(username='testuser', password='secret')
        response = self.c.get(reverse('agreementtext_index'))
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
        data = {'title': 'TEST', 'text': 'Test Test Test', 'var_name1': ''}
        response = self.c.post(reverse('add_agreement_text'), data)
        self.assertIsNone(response.context)

    def test_add_post_no_title_agreement_text(self):
        self.c.login(username='testuser', password='secret')
        data = {'text': 'Test Test Test', 'var_name1': ''}
        response = self.c.post(reverse('add_agreement_text'), data)
        self.assertIsNotNone(response.context['error'])

    def test_add_post_no_text_agreement_text(self):
        self.c.login(username='testuser', password='secret')
        data = {'title': 'TEST', 'var_name1': ''}
        response = self.c.post(reverse('add_agreement_text'), data)
        self.assertIsNotNone(response.context['error'])
