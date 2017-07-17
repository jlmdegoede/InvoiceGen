from datetime import datetime

from django.utils import timezone
from django_tables2 import RequestConfig

from agreements.models import Agreement

from .models import Product
from .tables import OrderTable


def get_previous_years(last_year):
    """Gets remaining years for orders not present in the index table tabs"""
    new_date = datetime(year=last_year, month=1, day=1)
    products = Product.objects.filter(date_deadline__lt=new_date)
    return set([x.date_deadline.year for x in products])


def fill_product_table_per_year(request, last_year):
    year_list = []
    products = {}

    now = timezone.now()

    for year in range(last_year, now.year + 1):
        products_year = Product.objects.filter(date_deadline__contains=year, done=True)
        if products_year.count() is not 0:
            year_list.append(year)
            products_year = add_agreements_to_products(products_year)
            prefix = str(year) + '-'
            products[year] = OrderTable(products_year, prefix=prefix, order_by='-date_deadline')
            RequestConfig(request).configure(products[year])

    year_list.sort(reverse=True)
    return products, year_list


def add_agreements_to_products(products):
    for product in products:
        add_agreements_to_product(product)
    return products


def add_agreements_to_product(product):
    agreements = Agreement.objects.filter(article_concerned=product)
    if agreements.count() != 0:
        product.agreement = agreements[0]
    return product
