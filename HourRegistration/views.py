from django.shortcuts import render
from .models import HourRegistration
from Orders.models import Product
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def start_time_tracking(request, product_id):
    product = Product.objects.get(id=product_id)
    time = HourRegistration(product=product, start=datetime.datetime.now())
    time.save()
    return JsonResponse({'success': True, 'start': time.start})


@login_required
def end_time_tracking(request, product_id):
    product = Product.objects.get(id=product_id)
    time = HourRegistration.objects.filter(product=product, end=None)
    if time.count() > 0:
        time = time[0]
    if not time.end:
        time.end = datetime.datetime.now()
        time.save()
    return JsonResponse({'success': True})
