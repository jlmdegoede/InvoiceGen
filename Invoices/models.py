from django.db import models

# Create your models here.
class Company(models.Model):
    bedrijfsnaam = models.CharField(max_length=200)
    bedrijfsadres = models.CharField(max_length=200)
    bedrijfsplaats_en_postcode = models.CharField(max_length=200)

    def __str__(self):
        return self.bedrijfsnaam


class Invoice(models.Model):
    title = models.CharField(max_length=200)
    date_created = models.DateField()
    to_company = models.ForeignKey(to=Company)
    contents = models.TextField()
    invoice_number = models.IntegerField()
    total_amount = models.IntegerField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.Invoice