from django.db import models
from Tenants.models import *
# Create your models here.


class Payment(models.Model):
    OPEN = 0
    ACTIVE = 1
    PAID = 2
    CANCELLED = 3
    PAYMENT_STATUS = (
        (OPEN, 'Open'),
        (ACTIVE, 'Actief'),
        (PAID, 'Betaald'),
        (CANCELLED, 'Geannuleerd')
    )
    amount = models.DecimalField(verbose_name='Hoeveelheid', max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(to=Client)
    status = models.IntegerField(choices=PAYMENT_STATUS, default=0)
    order_nr = models.IntegerField()

    def __str__(self):
        return 'Betaling van {!s} gemaakt op {!s}'.format(self.customer.subdomain, str(self.created))
