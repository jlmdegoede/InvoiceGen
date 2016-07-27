from django.shortcuts import render
from .models import HourRegistration
from Orders.models import Product
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def start_time_tracking(request, product_id):
    product = Product.objects.get(id=product_id)
    existing_time = HourRegistration.objects.filter(end=None)
    if existing_time.count() == 0:
        time = HourRegistration(product=product, start=timezone.now())
        time.save()
        return JsonResponse({'success': True, 'start': format_time_to_local(time.start)})
    else:
        return existing_time_tracking(request)


@login_required
def end_time_tracking(request, product_id):
    product = Product.objects.get(id=product_id)
    time = HourRegistration.objects.filter(product=product, end=None)
    if time.count() > 0:
        time = time[0]
    if not time.end:
        time.end = timezone.now()
        time.save()
    return JsonResponse({'success': True})


@login_required
def add_description_to_hourregistration(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        product = Product.objects.get(id=product_id)
        time = HourRegistration.objects.filter(product=product, end=None)
        if time.count() > 0:
            time = time[0]
        description = request.POST['description']
        time.description = description
        time.save()
        return JsonResponse({'success': True})
    if request.method == 'GET':
        product_id = request.GET['product_id']
        product = Product.objects.get(id=product_id)
        time = HourRegistration.objects.filter(product=product, end=None)
        if time.count() > 0:
            time = time[0]
        return JsonResponse({'description': time.description})


@login_required
def existing_time_tracking(request):
    time = HourRegistration.objects.filter(end=None)
    if time.count() > 0:
        time = time[0]
        product = Product.objects.get(id=time.product_id)
        return JsonResponse({'pk': time.product_id, 'start': format_time_to_local(time.start), 'title': product.title})
    return JsonResponse({"existing": False})


@login_required
def delete_time_tracking(request):
    time_id = request.POST['time_id']
    time = HourRegistration.objects.get(pk=time_id)
    time.delete()
    return JsonResponse({'success': True})


@login_required
def set_end_time(request):
    enddate = request.POST['endDate']
    endtime = request.POST['endTime']
    hour_id = request.POST['pk']
    if enddate and endtime and hour_id:
        end_date = format_date_and_time(enddate, endtime)
        time = HourRegistration.objects.get(pk=hour_id)
        time.end = end_date
        time.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def create_new_hour_registration(request):
    startdate = request.POST['startDate']
    starttime = request.POST['startTime']
    enddate = request.POST['endDate']
    endtime = request.POST['endTime']
    description = request.POST['description']
    product_id = request.POST['product_id']
    if enddate and endtime and product_id:
        start_date = format_date_and_time(startdate, starttime)
        end_date = format_date_and_time(enddate, endtime)
        product = Product.objects.get(pk=product_id)
        time = HourRegistration(start=start_date, end=end_date, product=product, description=description)
        time.save()
        return JsonResponse({'success': True})


def format_time_to_local(time):
    return timezone.localtime(time).strftime('%d-%m-%Y %H:%M:%S')


def format_date_and_time(date, time):
    return datetime.strptime(date + ' ' + time, '%d-%m-%Y %H:%M')