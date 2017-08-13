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
    payment_amount = models.DecimalField()


class BunqRequest(models.Model):
    counterparty_email = models.EmailField(null=True)
    counterparty_iban = models.CharField(max_length=34, null=True)
    counterparty_phone = models.CharField(max_length=34, null=True)
    to_company = models.ForeignKey(to=Company)
    bunq_request_id = models.IntegerField()
    description = models.TextField(blank=True)
