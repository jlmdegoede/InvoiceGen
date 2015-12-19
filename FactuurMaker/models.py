from django.db import models


class Invoice(models.Model):
    date_created = models.DateField()
    to_address = models.TextField(default="")
    from_address = models.TextField(default="")
    contents = models.TextField()
    invoice_number = models.IntegerField()
    total_amount = models.IntegerField()


class Article(models.Model):
    title = models.CharField(max_length=200)
    date_received = models.DateField()
    date_deadline = models.DateField()
    word_count = models.IntegerField()
    magazine = models.CharField(max_length=40)
    magazine_number = models.IntegerField()
    invoice = models.ForeignKey(Invoice, null=True, blank=True)
    paid = models.BooleanField(default=False)
    briefing = models.TextField(blank=True)
    done = models.BooleanField(default=False)
    word_price = models.FloatField(default=0.25)

    def __str__(self):
        return self.title

    def serialize(self):
        return {"title": self.title, "date": str(self.date_received), "deadline": str(self.date_deadline),
            "done": str(self.done), "magazine": self.magazine, "magazine_nr": self.magazine_number,
            "article_id": self.id, "wordcount": self.word_count, "briefing": self.briefing,
            "invoice_sent": self.invoice is not None}


class UserSetting(models.Model):
    naam = models.CharField(max_length=200)
    adres = models.CharField(max_length=200)
    woonplaats = models.CharField(max_length=200)
    emailadres = models.CharField(max_length=200)
    iban = models.CharField(max_length=200)


class CompanySetting(models.Model):
    bedrijfsnaam = models.CharField(max_length=200)
    bedrijfsadres = models.CharField(max_length=200)
    bedrijfsplaats = models.CharField(max_length=200)


