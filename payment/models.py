from django.db import models

from invoices.models import OutgoingInvoice
from companies.models import Company


class Payment(models.Model):
    PAID = 'paid'
    CANCELLED = 'cancelled'
    PENDING = 'pending'
    PAYMENT_STATUS = (
        (PAID, 'Betaald'),
        (CANCELLED, 'Geannuleerd'),
        (PENDING, 'Gemaakt')
    )

    created = models.DateTimeField(auto_now_add=True)
    for_invoice = models.ForeignKey(to=OutgoingInvoice)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    payment_amount = models.DecimalField(max_digits=99, decimal_places=2)

    def get_absolute_url(self):
        return self.for_invoice.get_absolute_url()


class BunqRequest(Payment):
    counterparty_email = models.EmailField(null=True)
    counterparty_iban = models.CharField(max_length=34, null=True)
    counterparty_phone = models.CharField(max_length=34, null=True)
    to_company = models.ForeignKey(to=Company)
    bunq_request_id = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return "Betaling via bunq request gemaakt op {0} met status {1}".format(self.created, self.status)


class MolliePayment(Payment):
    payment_id = models.IntegerField()

    def __str__(self):
        return "Betaling met iDEAL met status {0} gemaakt op {1}".format(self.created, self.status)
