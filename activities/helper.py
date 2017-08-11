from orders.models import Product
from datetime import datetime, timedelta


def recent_order_activities():
    recent_products = Product.objects.filter(done=False).order_by('-id')[:5]
    for product in recent_products:
        product.message = "Nieuwe opdracht {0} binnengekomen op {1}".format(product.title, product.date_received)
    return recent_products


def deadline_order_activities():
    today = datetime.now()
    next_week = today + timedelta(days=7)
    products_near_deadline = Product.objects.filter(done=False, date_deadline__lte=next_week)
    for product in products_near_deadline:
        product.message = 'Opdracht {0} nadert deadline van {1}'.format(product.title, product.date_deadline)
    return products_near_deadline
