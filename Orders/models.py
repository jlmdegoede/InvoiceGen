from django.db import models
from Invoices.models import Invoice
from Companies.models import Company


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

    def get_price(self):
        return float(self.price_per_quantity * self.quantity)

    def serialize(self):
        return {"title": self.title, "date": str(self.date_received), "deadline": str(self.date_deadline),
            "done": str(self.done), "magazine": self.magazine, "magazine_nr": self.magazine_number,
            "wordcount": self.word_count, "briefing": self.briefing, "server_id": self.id}


