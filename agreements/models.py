from django.db import models
from markdownx.models import MarkdownxField

from companies.models import Company
from orders.models import Product


class AgreementTextVariable(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AgreementText(models.Model):
    title = models.CharField(max_length=300)
    text = MarkdownxField()
    edited_at = models.DateTimeField()
    variables = models.ManyToManyField(to=AgreementTextVariable)

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ('view_agreementtext', 'Kan modelovereenkomst aanmaken'),
        )


class AgreementVariableInstance(models.Model):
    variable = models.ForeignKey(to=AgreementTextVariable)
    value = models.TextField(blank=True)


class Agreement(models.Model):
    agreement_text = models.ForeignKey(to=AgreementText)
    agremeent_text_variables = models.ManyToManyField(to=AgreementVariableInstance)
    agreement_text_copy = models.TextField()
    article_concerned = models.ManyToManyField(to=Product)
    client_name = models.CharField(max_length=200)
    client_emailaddress = models.CharField(max_length=200)
    company = models.ForeignKey(to=Company)
    created = models.DateTimeField(auto_now_add=True)
    signed_by_client = models.BooleanField(default=False)
    signed_by_client_at = models.DateTimeField(null=True)
    signature_file_client = models.ImageField(null=True, upload_to='signatures')
    signature_file_contractor = models.ImageField(null=True, upload_to='signatures')
    signed_by_contractor = models.BooleanField(default=False)
    signed_by_contractor_at = models.DateTimeField(null=True)
    url = models.CharField(max_length=50)

    def __str__(self):
        return "Overeenkomst met {0} gemaakt op {1}".format(self.company.company_name,
                                                            self.created.strftime('%m-%d-%Y'))

    class Meta:
        permissions = (
            ('view_agreement', 'Kan overeenkomst bekijken'),
        )
