from django.shortcuts import render
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from Invoices.models import IncomingInvoice
from Utils.date_helper import get_formatted_string
from HourRegistration.models import *
from django.db.models import Q
import itertools
import pytz
# Create your views here.


@login_required
def view_statistics(request):
    year = date.today().year
    year_list = [int(year) - 5, int(year) - 4, int(year) - 3, int(year) - 2, int(year) - 1, int(year)]
    nr_of_articles = []
    not_yet_invoiced = []
    nr_of_words = []
    totale_inkomsten = []

    total_hours = get_total_hours(year)

    for i in range(int(year) - 5, int(year) + 1):
        tuple = get_yearly_stats(i)
        nr_of_articles.append(tuple[0])
        nr_of_words.append(tuple[1])
        totale_inkomsten.append(tuple[2])
        not_yet_invoiced.append(tuple[3])
    return render(request, 'Statistics/statistics.html',
                  {'nr_of_articles': nr_of_articles, 'not_yet_invoiced': not_yet_invoiced, 'nr_of_words': nr_of_words,
                   'totale_inkomsten': totale_inkomsten, 'year': year, 'year_list': year_list, 'total_hours': total_hours})


def get_total_hours(year, hour_registrations=None):
    if hour_registrations is None:
        hour_registrations = HourRegistration.objects.filter(Q(start__year=year) | Q(end__year=year))

    hour_registrations = get_unique_hours(hour_registrations, year)[1]
    total_hours = 0
    for hr in hour_registrations:
        end_date = set_end_date(hr.end, year)
        start_date = set_start_date(hr.start, year)

        hours_worked = end_date - start_date
        if hours_worked.total_seconds() >= 0:
            total_hours += hours_worked.total_seconds() / 3600
    return round(total_hours, 2)


def set_end_date(hr_end_date, year):
    end_date = hr_end_date
    if hr_end_date is None:
        end_date = timezone.now()
    if end_date.year >= year + 1:
        end_date = timezone.make_aware(timezone.datetime(year, 12, 31, 23, 59, 59))
    return end_date


def set_start_date(hr_start_date, year):
    start_date = hr_start_date
    if hr_start_date.year <= year - 1:
        start_date = timezone.make_aware(timezone.datetime(year, 1, 1, 00, 00, 00))
    return start_date


def split_list(a_list):
    half = int(len(a_list)/2)
    return a_list[:half], a_list[half:]


def get_unique_hours(hour_registrations, year):
    hour_registrations = list(hour_registrations)

    if len(hour_registrations) > 2:
        splitted_list = split_list(hour_registrations)
        check_tuple_one = get_unique_hours(splitted_list[0], year)
        check_tuple_two = get_unique_hours(splitted_list[1], year)

        if check_tuple_one[0] or check_tuple_two[0]:
            new_list = check_tuple_one[1] + check_tuple_two[1]
            return get_unique_hours(new_list, year)
        else:
            new_list = check_tuple_one[1] + check_tuple_two[1]
            return False, new_list
    elif len(hour_registrations) == 2:
        return get_overlapping_hours(hour_registrations[0], hour_registrations[1], year)
    else:
        return False, hour_registrations


def get_overlapping_hours(hr_one, hr_two, year):
    end_date1 = set_end_date(hr_one.end, year)
    start_date1 = set_start_date(hr_one.start, year)
    end_date2 = set_end_date(hr_two.end, year)
    start_date2 = set_start_date(hr_two.start, year)

    earliest_start = min(start_date1, start_date2)
    latest_end = max(end_date1, end_date2)

    if start_date1 <= end_date2 and start_date2 <= end_date1:
        return True, [HourRegistration(start=earliest_start, end=latest_end, product=hr_one.product)]
    return False, [hr_one, hr_two]


def get_longest_hr(hr_one, hr_two, year):
    if hr_one is None:
        return [hr_two]
    if hr_two is None:
        return [hr_one]

    end_date1 = set_end_date(hr_one.end, year)
    start_date1 = set_start_date(hr_one.start, year)
    end_date2 = set_end_date(hr_two.end, year)
    start_date2 = set_start_date(hr_two.start, year)

    timedelta_one = end_date1 - start_date1
    timedelta_two = end_date2 - start_date2

    return hr_one if timedelta_one > timedelta_two else hr_two


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


@login_required
def get_start_end_dates(request):
    start_date = None
    end_date = None
    if 'start_date' in request.POST and 'end_date' in request.POST:
        start_date = datetime.strptime(request.POST['start_date'], '%d-%m-%Y')
        end_date = datetime.strptime(request.POST['end_date'], '%d-%m-%Y')
    if not start_date or not end_date or end_date < start_date:
        now = timezone.now()
        quarter = (now.month - 1) // 3
        start_date = get_previous_quarter_start_date(now, quarter)
        end_date = get_previous_quarter_end_date(now, quarter)
    return start_date, end_date


@login_required
def view_btw_aangifte(request):
    start_date, end_date = get_start_end_dates(request)

    incoming_btw = get_btw_incoming(start_date, end_date)
    outgoing_btw = get_btw_outgoing(start_date, end_date)
    difference_btw = float(outgoing_btw) - float(incoming_btw)

    incoming_invoices = IncomingInvoice.objects.filter(received_date__gte=start_date, received_date__lte=end_date).exclude(btw_amount=0)

    outgoing_invoices = OutgoingInvoice.objects.filter(date_created__gte=start_date, date_created__lte=end_date)
    outgoing_invoices = [x for x in outgoing_invoices if x.get_btw() is not 0]

    return render(request, 'Statistics/btw_aangifte.html',
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
    invoices = IncomingInvoice.objects.filter(received_date__gte=start_date, received_date__lte=end_date).exclude(btw_amount=0)
    btw_incoming = 0
    for invoice in invoices:
        btw_incoming += invoice.btw_amount
    return btw_incoming


def get_previous_quarter_start_date(now, quarter):
    quarter = quarter - 1 if quarter - 1 >= 0 else 3 # rollover
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
