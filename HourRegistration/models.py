from django.db import models
from Orders.models import *
# Create your models here.


class HourRegistration(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    product = models.ForeignKey(to=Product)

    def number_of_hours(self):
        if self.end is not None:
            return str(self.end - self.start).split(".")[0]
        return "geen eindtijd"
