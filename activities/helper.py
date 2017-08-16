from orders.models import Product
from payment.models import Payment
from datetime import datetime, timedelta


def recent_order_activities():
    recent_products = Product.objects.filter(done=False).order_by('-id')[:5]
    for product in recent_products:
        product.message = "Nieuwe opdracht {0} binnengekomen op {1}".format(product.title,
                                                                            product.date_received.strftime("%d-%m-%Y"))
        product.compare_date = product.date_received
    return recent_products


def deadline_order_activities():
    today = datetime.now()
    next_week = today + timedelta(days=7)
    products_near_deadline = Product.objects.filter(done=False, date_deadline__lte=next_week)
    for product in products_near_deadline:
        product.message = 'Opdracht {0} nadert deadline van {1}'.format(product.title,
                                                                        product.date_deadline.strftime("%d-%m-%Y"))
        product.compare_date = product.date_deadline
    return products_near_deadline


def recent_paid_invoices():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    paid_last_week = Payment.objects.filter(status=Payment.PAID, created__gte=last_week)
    for paid in paid_last_week:
        paid.message = "Factuur {0} is betaald door {1} op {2} om {3}".format(str(paid.for_invoice.invoice_number),
                                                                            paid.for_invoice.to_company,
                                                                            paid.created.strftime("%d-%m-%Y"),
                                                                            paid.created.strftime("%H:%M"))
        paid.compare_date = paid.created.date()
    return paid_last_week
