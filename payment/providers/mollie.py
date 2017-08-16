import os, time

from django.shortcuts import reverse
from settings.helper import get_setting
from settings.const import SITE_URL, MOLLIE_API_KEY
import Mollie

from ..models import MolliePayment, Payment


class MollieApi(object):

    def __init__(self):
        api_key = get_setting(MOLLIE_API_KEY, '')
        if api_key:
            self.mollie = Mollie.API.Client()
            self.mollie.setApiKey(api_key)

    def create_request(self, invoice):
        payment_obj = MolliePayment()
        payment_obj.payment_id = int(time.time())
        payment_obj.payment_amount = invoice.get_total_amount()
        payment_obj.status = Payment.PENDING
        payment_obj.for_invoice = invoice
        webhook_url = get_setting(SITE_URL, '') + reverse('mollie_webhook')
        return_url = get_setting(SITE_URL, '') + reverse('mollie_return', kwargs={'invoice_id': invoice.id})
        payment = self.mollie.payments.create({
            'amount': payment_obj.payment_amount,
            'description': invoice.title,
            'redirectUrl': return_url,
            'webhookUrl': webhook_url,
            'method': Mollie.API.Object.Method.IDEAL,
            'metadata': {
                'payment_nr': payment_obj.payment_id,
            }
        })
        payment_obj.save()
        return payment.getPaymentUrl()

    def get_payment(self, id):
        return self.mollie.payments.get(id)
