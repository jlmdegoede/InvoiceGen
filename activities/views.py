from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from itertools import chain

from .helper import recent_order_activities, deadline_order_activities, recent_paid_invoices


@login_required
def index(request):
    recent_orders = recent_order_activities()
    deadline_orders = deadline_order_activities()
    paid_invoices = recent_paid_invoices()
    orders = sorted(chain(recent_orders, deadline_orders, paid_invoices), key=lambda instance: instance.compare_date, reverse=True)
    return render(request, 'activities/index.html', {'orders': orders})