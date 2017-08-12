from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from invoices.models import OutgoingInvoice

from .providers.mollie import MollieApi
from .providers.bunq import BunqApi


def mollie_payment(request, invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    mollie = MollieApi()
    redirect_url = mollie.create_request(invoice.get_total_amount(), invoice.title)
    return redirect(to=redirect_url)


@login_required
def bunq_request(request, invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    bunq_api = BunqApi()
    bunq_api.create_request(invoice.get_total_amount(), invoice.to_company.company_email, invoice.title)
    return JsonResponse({'request': 'created'})

