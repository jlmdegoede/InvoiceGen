import requests
from django.utils import timezone
from datetime import timedelta, datetime
import json
from django.shortcuts import render
from Utils.date_helper import get_formatted_string
from Settings.models import Setting
import pytz
from InvoiceGen.site_settings import COMMUNICATION_KEY


class OrderMiddleware(object):
    def process_response(self, request, response):
        utc = pytz.UTC
        check_existing = Setting.objects.filter(key='subscription_date')
        now = timezone.now()
        day_ago = now - timedelta(days=1)
        valid_until = None

        if check_existing.count() is not 0:
            subscription_date = check_existing[0]
            if subscription_date.last_updated_at > day_ago:
                valid_until = utc.localize(datetime.strptime(subscription_date.value, '%Y-%m-%d %H:%M:%S'))

        if check_existing.count() is 0 or valid_until is None:
            print('Value retrieved from server')
            req = requests.post('https://invoicegen.nl/get-subscription-status/', {'key': COMMUNICATION_KEY},
                                {})
            invoice_site = json.loads(req.content.decode('utf-8'))
            valid_until = utc.localize(datetime.strptime(invoice_site['valid_until'], '%Y-%m-%d'))
            setting = Setting.objects.create(key='subscription_date', value=valid_until)
            setting.save()

        if now > valid_until:
            return render(request, 'subscription_expired.html', {'valid_until': get_formatted_string(valid_until)})
        else:
            return response
