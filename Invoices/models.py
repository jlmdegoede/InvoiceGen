from django.db import models
from Companies.models import *


class Invoice(models.Model):
    title = models.CharField(max_length=200)
    date_created = models.DateField()
    to_company = models.ForeignKey(to=Company)
    contents = models.TextField()
    invoice_number = models.IntegerField()
    total_amount = models.IntegerField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.title