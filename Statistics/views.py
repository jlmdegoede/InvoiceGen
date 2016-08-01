from django.shortcuts import render
from datetime import date, datetime
from Orders.models import Product
from django.contrib.auth.decorators import login_required
from Invoices.models import OutgoingInvoice, IncomingInvoice
from Utils.date_helper import get_formatted_string

# Create your views here.


@login_required
def view_statistics(request):
    year = date.today().year
    year_list = [int(year) - 5, int(year) - 4, int(year) - 3, int(year) - 2, int(year) - 1, int(year)]
    nr_of_articles = []
    not_yet_invoiced = []
    nr_of_words = []
    totale_inkomsten = []
    totale_urenbesteding = 0

    for i in range(int(year) - 5, int(year) + 1):
        tuple = get_yearly_stats(i)
        nr_of_articles.append(tuple[0])
        nr_of_words.append(tuple[1])
        totale_inkomsten.append(tuple[2])
        not_yet_invoiced.append(tuple[3])
    return render(request, 'statistics.html',
                  {'nr_of_articles': nr_of_articles, 'not_yet_invoiced': not_yet_invoiced, 'nr_of_words': nr_of_words,
                   'totale_inkomsten': totale_inkomsten, 'year': year, 'year_list': year_list})


def get_yearly_stats(year):
    nr_of_articles = 0
    totale_inkomsten = 0
    nr_of_words = 0
    all_products = Product.objects.filter(done=True)
    for product in all_products:
        if product.date_deadline.year == int(year):
            totale_inkomsten += product.quantity * product.price_per_quantity
            nr_of_words += product.quantity
            nr_of_articles += 1
    not_yet_invoiced = 0
    not_yet_invoiced_articles = Product.objects.filter(done=False)
    for article in not_yet_invoiced_articles:
        not_yet_invoiced += article.quantity * article.price_per_quantity

    return nr_of_articles, nr_of_words, totale_inkomsten, not_yet_invoiced


def get_start_end_dates(request):
    start_date = None
    end_date = None
    if 'start_date' in request.POST and 'end_date' in request.POST:
        start_date = datetime.strptime(request.POST['start_date'], '%d-%m-%Y')
        end_date = datetime.strptime(request.POST['end_date'], '%d-%m-%Y')
    if not start_date or not end_date or end_date < start_date:
        now = datetime.now()
        quarter = (now.month - 1) // 3
        start_date = get_previous_quarter_start_date(now, quarter)
        end_date = get_previous_quarter_end_date(now, quarter)
    return start_date, end_date


def view_btw_aangifte(request):
    start_date, end_date = get_start_end_dates(request)

    incoming_btw = get_btw_incoming(start_date, end_date)
    outgoing_btw = get_btw_outgoing(start_date, end_date)
    difference_btw = float(outgoing_btw) - float(incoming_btw)

    incoming_invoices = IncomingInvoice.objects.filter(date_created__gte=start_date, date_created__lte=end_date).exclude(btw_amount=0)

    outgoing_invoices = OutgoingInvoice.objects.filter(date_created__gte=start_date, date_created__lte=end_date)
    outgoing_invoices = filter(lambda x: x.get_btw() is not 0, outgoing_invoices)

    return render(request, 'btw_aangifte.html',
                  {'incoming_btw': incoming_btw, 'outgoing_btw': outgoing_btw, 'difference_btw': str(difference_btw),
                   'incoming_invoices': incoming_invoices, 'outgoing_invoices': outgoing_invoices,
                   'start_date': get_formatted_string(start_date), 'end_date': get_formatted_string(end_date)})


def get_btw_outgoing(start_date, end_date):
    invoices = OutgoingInvoice.objects.filter(date_created__gte=start_date, date_created__lte=end_date)
    btw_outgoing = 0
    for invoice in invoices:
        btw_outgoing += invoice.get_btw()
    return btw_outgoing


def get_btw_incoming(start_date, end_date):
    invoices = IncomingInvoice.objects.filter(date_created__gte=start_date, date_created__lte=end_date).exclude(btw_amount=0)
    btw_incoming = 0
    for invoice in invoices:
        btw_incoming += invoice.btw_amount
    return btw_incoming


def get_previous_quarter_start_date(now, quarter):
    quarter = quarter - 1 if quarter - 1 >= 0 else 3
    year = now.year if quarter >= 0 else now.year - 1

    quarters = {
        0: datetime(year, 1, 1),
        1: datetime(year, 4, 1),
        2: datetime(year, 7, 1),
        3: datetime(year, 10, 1),
    }
    return quarters.get(quarter, 0)


def get_previous_quarter_end_date(now, quarter):
    quarter = quarter - 1 if quarter - 1 >= 0 else 3
    year = now.year if quarter >= 0 else now.year - 1

    quarters = {
        0: datetime(year, 3, 31),
        1: datetime(year, 6, 30),
        2: datetime(year, 9, 30),
        3: datetime(year, 12, 31),
    }
    return quarters.get(quarter, 0)
