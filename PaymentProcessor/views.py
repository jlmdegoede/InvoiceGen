from django.shortcuts import render, redirect
import Mollie
from .models import Payment
from Tenants.models import *
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
import requests
# Create your views here.

API_KEY = 'live_MWPCMjkbQP98tnGCMy7QHPN8kxQQ9R'
TEST_API_KEY = 'test_aKWPvDzksSkfkKBmDCDytArtg7x29T'


def start_mollie_payment(request):
    if request.method == 'GET':
        if 'key' not in request.GET:
            return JsonResponse({'error': 'Invalid communication key provided'})

        invoice_site = InvoiceSite.objects.filter(communication_key=request.GET['key'])

        if invoice_site.count() is 0:
            return JsonResponse({'error': 'Invalid communication key provided'})
        else:
            invoice_site = invoice_site[0]

        mollie = Mollie.API.Client()
        mollie.setApiKey(API_KEY)

        payment_obj = Payment()
        payment_obj.amount = 5.00
        payment_obj.customer = invoice_site
        payment_obj.order_nr = invoice_site.customer_number + int(time.time())

        payment_obj.save()

        payment = mollie.payments.create({
            'amount': payment_obj.amount,
            'description': '1 maand InvoiceGen.nl',
            'webhookUrl': 'https://invoicegen.nl/betaling/status/',
            'redirectUrl': 'https://invoicegen.nl/betaling/succes?order_nr=' + str(payment_obj.order_nr),
            'metadata': {
                'order_nr': payment_obj.order_nr
            }
        })

        return redirect(payment.getPaymentUrl())


@csrf_exempt
def status_change_mollie_payment(request):
    mollie = Mollie.API.Client()
    mollie.setApiKey(API_KEY)
    payment = mollie.payments.get(request.POST['id'])

    order_nr = payment['metadata']['order_nr']
    payment_obj = Payment.objects.get(order_nr=order_nr)

    if payment.isPending():
        payment_obj.status = Payment.ACTIVE
    if payment.isOpen():
        payment_obj.status = Payment.ACTIVE
    if payment.isPaid():
        payment_obj.status = Payment.PAID
        invoice_site = payment_obj.customer
        invoice_site.add_days_to_subscription(31)
        invoice_site.save()
    else:
        payment_obj.status = Payment.CANCELLED
    payment_obj.save()

    return JsonResponse({'success': 'true'})


def complete_change_mollie_payment(request):
    if 'order_nr' in request.GET:
        payment = Payment.objects.get(order_nr=request.GET['order_nr'])
        invoice_site_url = payment.customer.get_complete_url('')
        return render(request, 'payment_result.html', {'order_nr': payment.order_nr, 'status': Payment.PAYMENT_STATUS[payment.status][1], 'url': invoice_site_url})
