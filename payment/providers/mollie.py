import os, time

import Mollie


class MollieApi(object):

    def __init__(self):
        self.mollie = Mollie.API.Client()
        self.mollie.setApiKey(os.getenv('MOLLIE_API_KEY'))

    def create_request(self, request_amount, description):
        order_nr = int(time.time())
        payment = self.mollie.payments.create({
            'amount': request_amount,
            'description': description,
            'redirectUrl': 'https://webshop.example.org/order/12345/',
            'webhookUrl': 'https://webshop.example.org/mollie-webhook/',
            'method': Mollie.API.Object.Method.IDEAL,
        })
        return payment.getPaymentUrl()
