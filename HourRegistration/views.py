from django.shortcuts import render
from .models import HourRegistration
from Orders.models import Product
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def start_time_tracking(request, product_id):
    product = Product.objects.get(id=product_id)
    existing_time = HourRegistration.objects.filter(end=None)
    if existing_time.count() == 0:
        time = HourRegistration(product=product, start=datetime.datetime.now())
        time.save()
        return JsonResponse({'success': True, 'start': time.start.strftime('%d-%m-%Y %H:%M:%S')})
    else:
        return existing_time_tracking(request)


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


@login_required
def existing_time_tracking(request):
    time = HourRegistration.objects.filter(end=None)
    if time.count() > 0:
        time = time[0]
        product = Product.objects.get(id=time.product_id)
        return JsonResponse({'pk': time.product_id, 'start': time.start.strftime('%d-%m-%Y %H:%M:%S'), 'title': product.title})
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
        end_date = datetime.datetime.strptime(enddate + ' ' + endtime, '%d-%m-%Y %H:%M')
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
    product_id = request.POST['product_id']
    if enddate and endtime and product_id:
        start_date = datetime.datetime.strptime(startdate + ' ' + starttime, '%d-%m-%Y %H:%M')
        end_date = datetime.datetime.strptime(enddate + ' ' + endtime, '%d-%m-%Y %H:%M')
        product = Product.objects.get(pk=product_id)
        time = HourRegistration(start=start_date, end=end_date, product=product)
        time.save()
        return JsonResponse({'success': True})
