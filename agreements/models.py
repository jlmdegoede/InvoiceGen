from django.db import models
from orders.models import Product
from companies.models import Company
# Create your models here.


class AgreementText(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField()
    edited_at = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ('view_agreementtext', 'Kan modelovereenkomst aanmaken'),
        )


class Agreement(models.Model):
    agree_text = models.ForeignKey(to=AgreementText)
    signed_by_client = models.BooleanField(default=False)
    signed_by_client_at = models.DateTimeField(null=True)
    signature_file_client = models.ImageField(null=True, upload_to='signatures')
    signature_file_contractor = models.ImageField(null=True, upload_to='signatures')
    signed_by_contractor = models.BooleanField(default=False)
    signed_by_contractor_at = models.DateTimeField(null=True)
    client_name = models.CharField(max_length=200)
    client_emailaddress = models.CharField(max_length=200)
    company = models.ForeignKey(to=Company)
    article_concerned = models.ManyToManyField(to=Product)
    agreement_text_copy = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=50)

    def __str__(self):
        return "Overeenkomst met {0} gemaakt op {1}".format(self.company.company_name,
                                                            self.created.strftime('%m-%d-%Y'))

    class Meta:
        permissions = (
            ('view_agreement', 'Kan overeenkomst bekijken'),
        )
