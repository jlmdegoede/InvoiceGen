from .models import HourRegistration
from orders.models import Product
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
import pytz
from django.contrib.auth.decorators import permission_required


@login_required
@permission_required('hour_registration.add_hourregistration', 'hour_registration.change_hourregistration')
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
@permission_required('hour_registration.change_hourregistration')
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
@permission_required('hour_registration.change_hourregistration')
def add_description_to_hourregistration(request):
    if request.method == 'POST':
        return add_description_to_hourregistration_post(request)
    if request.method == 'GET':
        return get_description_to_hourregistration(request)


def add_description_to_hourregistration_post(request):
    product_id = request.POST['product_id']
    product = Product.objects.get(id=product_id)
    time = HourRegistration.objects.filter(product=product, end=None)
    if time.count() > 0:
        time = time[0]
        description = request.POST['description']
        time.description = description
        time.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'No open HR found'})


def get_description_to_hourregistration(request):
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    time = HourRegistration.objects.filter(product=product, end=None)
    if time.count() > 0:
        time = time[0]
        return JsonResponse({'description': time.description})
    return JsonResponse({'error': 'No HR object found'})


@login_required
@permission_required('hour_registration.view_hourregistration')
def existing_time_tracking(request):
    time = HourRegistration.objects.filter(end=None).first()
    if time is not None:
        product = Product.objects.get(id=time.product_id)
        return JsonResponse({'pk': time.product_id, 'start': format_time_to_local(time.start), 'title': product.title})
    return JsonResponse({"existing": 'False'})


@login_required
@permission_required('hour_registration.delete_hourregistration')
def delete_time_tracking(request):
    try:
        time_id = request.POST['time_id']
        time = HourRegistration.objects.get(pk=time_id)
        time.delete()
        return JsonResponse({'success': 'true'})
    except HourRegistration.DoesNotExist:
        return JsonResponse({'error': 'HR object not found'})


@login_required
@permission_required('hour_registration.change_hourregistration')
def set_end_time(request):
    if 'pk' in request.POST and 'endDate' in request.POST and 'endTime' in request.POST:
        enddate = request.POST['endDate']
        endtime = request.POST['endTime']
        hour_id = request.POST['pk']
        end_date = format_date_and_time(enddate, endtime)
        time = HourRegistration.objects.get(pk=hour_id)
        time.end = pytz.timezone('Europe/Amsterdam').localize(end_date)
        time.save()
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success': 'false'})


@login_required
@permission_required('hour_registration.add_hourregistration')
def create_new_hour_registration(request):
    if 'startDate' in request.POST and 'startTime' in request.POST \
            and 'endDate' in request.POST \
            and 'endTime' in request.POST \
            and 'product_id' in request.POST:
        startdate = request.POST['startDate']
        starttime = request.POST['startTime']
        enddate = request.POST['endDate']
        endtime = request.POST['endTime']
        product_id = request.POST['product_id']

        description = ""
        if 'description' in request.POST:
            description = request.POST['description']

        start_date = format_date_and_time(startdate, starttime)
        end_date = format_date_and_time(enddate, endtime)
        product = Product.objects.get(pk=product_id)
        time = HourRegistration(start=start_date, end=end_date, product=product, description=description)
        time.save()

        return JsonResponse({'success': 'true'})
    return JsonResponse({'success': 'false'})


def format_time_to_local(time):
    return timezone.localtime(time).strftime('%d-%m-%Y %H:%M:%S')


def format_date_and_time(date, time):
    return datetime.strptime(date + ' ' + time, '%d-%m-%Y %H:%M')
