from django.db import models
from Orders.models import *
# Create your models here.


class HourRegistration(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    product = models.ForeignKey(to=Product)
