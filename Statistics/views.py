from django.shortcuts import render
from datetime import date
from Orders.models import Product
from django.contrib.auth.decorators import login_required
from Invoices.models import OutgoingInvoice, IncomingInvoice


# Create your views here.


@login_required
def view_statistics(request):
    year = date.today().year
    year_list = [int(year) - 5, int(year) - 4, int(year) - 3, int(year) - 2, int(year) - 1, int(year)]
    nr_of_articles = []
    not_yet_invoiced = []
    nr_of_words = []
    totale_inkomsten = []
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
    all_articles = Product.objects.filter(done=True)
    for article in all_articles:
        if article.date_deadline.year == int(year):
            totale_inkomsten += article.quantity * article.price_per_quantity
            nr_of_words += article.quantity
            nr_of_articles += 1
    not_yet_invoiced = 0
    not_yet_invoiced_articles = Product.objects.filter(done=False)
    for article in not_yet_invoiced_articles:
        not_yet_invoiced += article.quantity * article.price_per_quantity

    return nr_of_articles, nr_of_words, totale_inkomsten, not_yet_invoiced


def view_btw_aangifte(request):
    year = 2016
    incoming_btw = get_btw_incoming(year)
    outgoing_btw = get_btw_outgoing(year)
    difference_btw = float(outgoing_btw) - float(incoming_btw)

    incoming_invoices = IncomingInvoice.objects.filter(date_created__year=year)
    outgoing_invoices = OutgoingInvoice.objects.filter(date_created__year=year)
    return render(request, 'btw_aangifte.html',
                  {'incoming_btw': incoming_btw, 'outgoing_btw': outgoing_btw, 'difference_btw': str(difference_btw),
                   'incoming_invoices': incoming_invoices, 'outgoing_invoices': outgoing_invoices})


def get_btw_outgoing(year):
    invoices = OutgoingInvoice.objects.filter(date_created__year=year)
    btw_outgoing = 0
    for invoice in invoices:
        btw_outgoing += invoice.get_btw()
    return btw_outgoing


def get_btw_incoming(year):
    invoices = IncomingInvoice.objects.filter(date_created__year=year)
    btw_incoming = 0
    for invoice in invoices:
        btw_incoming += invoice.btw_amount
    return btw_incoming
