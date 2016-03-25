from django.db import models

# Create your models here.


class Magazine(models.Model):
    titel = models.CharField(max_length=200)

    def serialize(self):
        return {"title": self.titel, "id": self.id}


class MagazineUitgave(models.Model):
    nummer = models.CharField(max_length=10)
    magazine = models.ForeignKey(Magazine)
    verschijningsdatum = models.DateField()

    def serialize(self):
        return {"nummer": self.nummer, "magazine": self.magazine,
                "verschijningsdatum": self.verschijningsdatum, "id":self.id}
