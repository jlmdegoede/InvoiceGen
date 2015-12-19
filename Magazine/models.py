from django.db import models

# Create your models here.


class Magazine(models.Model):
    titel = models.CharField(max_length=200)


class MagazineUitgave(models.Model):
    nummer = models.CharField(max_length=10)
    magazine = models.ForeignKey(Magazine)
    verschijningsdatum = models.DateField()
