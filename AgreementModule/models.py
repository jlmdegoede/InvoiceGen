from django.db import models
from FactuurMaker.models import Product
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
    client_name = models.CharField(max_length=200)
    client_emailaddress = models.CharField(max_length=200)
    article_concerned = models.ManyToManyField(to=Product)
    agreement_text_copy = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=50)
