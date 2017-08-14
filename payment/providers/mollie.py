import os, time

from django.shortcuts import reverse
import Mollie

from ..models import MolliePayment, Payment


class MollieApi(object):

    def __init__(self):
        self.mollie = Mollie.API.Client()
        self.mollie.setApiKey(os.getenv('MOLLIE_API_KEY'))

    def create_request(self, invoice):
        payment_obj = MolliePayment()
        payment_obj.payment_id = int(time.time())
        payment_obj.payment_amount = invoice.get_total_amount()
        payment_obj.status = Payment.PENDING
        payment_obj.for_invoice = invoice
        webhook_url = 'http://debf641e.ngrok.io' + reverse('mollie_webhook')
        return_url = 'http://debf641e.ngrok.io' + reverse('mollie_return', kwargs={'invoice_id': invoice.id})
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
