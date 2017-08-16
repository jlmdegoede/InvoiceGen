from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from invoices.models import OutgoingInvoice

from .providers.mollie import MollieApi
from .providers.bunq import BunqApi
from .models import MolliePayment


def mollie_payment(request, invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    mollie = MollieApi()
    redirect_url = mollie.create_request(invoice)
    return redirect(to=redirect_url)


@login_required
def bunq_request(request, invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    bunq_api = BunqApi()
    bunq_api.create_request(invoice)
    return JsonResponse({'request': 'created'})


@csrf_exempt
def mollie_webhook(request):
    mollie = MollieApi()
    payment_id = request.POST['id']
    payment = mollie.get_payment(payment_id)
    payment_nr = payment['metadata']['payment_nr']
    payment_obj = MolliePayment.objects.get(payment_id=payment_nr)

    if payment.isPaid():
        payment_obj.status = MolliePayment.PAID
        payment_obj.for_invoice.paid = True
        payment_obj.for_invoice.save()
    elif payment.isPending() or payment.isOpen():
        payment_obj.status = MolliePayment.PENDING
    else:
        payment_obj.status = MolliePayment.CANCELLED
    payment_obj.save()
    return JsonResponse({'webhook': 'received'})


def mollie_return(request, invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    return redirect(to=invoice.get_complete_url())
