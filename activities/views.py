from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from itertools import chain

from .helper import recent_order_activities, deadline_order_activities


@login_required
def index(request):
    recent_orders = recent_order_activities()
    deadline_orders = deadline_order_activities()
    orders = sorted(chain(recent_orders, deadline_orders), key=lambda instance: instance.date_deadline, reverse=True)
    return render(request, 'activities/index.html', {'orders': orders})