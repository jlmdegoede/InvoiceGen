from django.db import models
from Orders.models import Product
from Companies.models import Company
# Create your models here.


class AgreementText(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField()
    edited_at = models.DateTimeField()

    def __str__(self):
        return self.title


class Agreement(models.Model):
    agree_text = models.ForeignKey(to=AgreementText)
    signed_by_client = models.BooleanField(default=False)
    signed_by_client_at = models.DateTimeField(null=True)
    signature_file = models.ImageField(null=True, upload_to='signatures')
    client_name = models.CharField(max_length=200)
    client_emailaddress = models.CharField(max_length=200)
    company = models.ForeignKey(to=Company)
    article_concerned = models.ManyToManyField(to=Product)
    agreement_text_copy = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=50)

    def __str__(self):
        return "Overeenkomst met " + self.company.company_name + " gemaakt op " + self.created.strftime('%m-%d-%Y')
