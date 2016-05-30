from django.db import models
from Invoices.models import Invoice, Company

class Product(models.Model):
    title = models.CharField(max_length=200)
    date_received = models.DateField()
    date_deadline = models.DateField()
    quantity = models.IntegerField()
    from_company = models.ForeignKey(to=Company, null=True, blank=True)
    identification_number = models.IntegerField(null=True)
    invoice = models.ForeignKey(Invoice, null=True, blank=True)
    briefing = models.TextField(blank=True)
    done = models.BooleanField(default=False)
    price_per_quantity = models.FloatField()
    tax_rate = models.IntegerField()

    def __str__(self):
        return self.title

    def serialize(self):
        return {"title": self.title, "date": str(self.date_received), "deadline": str(self.date_deadline),
            "done": str(self.done), "magazine": self.magazine, "magazine_nr": self.magazine_number,
            "wordcount": self.word_count, "briefing": self.briefing, "server_id": self.id}


class UserSetting(models.Model):
    naam = models.CharField(max_length=200)
    adres = models.CharField(max_length=200)
    plaats_en_postcode = models.CharField(max_length=200)
    emailadres = models.CharField(max_length=200)
    iban = models.CharField(max_length=200)
    site_name = models.CharField(max_length=50, default='InvoiceGen')


