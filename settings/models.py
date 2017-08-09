from django.db import models

# Create your models here.


class UserSetting(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city_and_zipcode = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    iban = models.CharField(max_length=200)
    kvk = models.CharField(max_length=10, null=True)
    btw_number = models.CharField(max_length=30, null=True)


class Setting(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    last_updated_at = models.DateTimeField(auto_now=True)
