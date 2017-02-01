from django.shortcuts import render
from .models import Client
from django.shortcuts import *
import subprocess
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils.text import slugify
import string
import random
from Blog.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.views.generic import View
# Create your views here.

def create_public_tenant(request):
    tenant = Client(domain_url='invoicegen.nl', # don't add your port or www here! on a local server you'll want to use localhost here
                    schema_name='public',
                    first_name='Schemas Inc.',
                    last_name='Test',
                    email='test@test.test',
                    active=True,
                    customer_number=102400,
                    valid_until='2018-12-05',
                    on_trial=False)
    tenant.save() # migrate_schemas automatically called, your tenant is ready to be used!
    tenant = Client(domain_url='jochemdegoede.invoicegen.nl', # don't add your port or www here! on a local server you'll want to use localhost here
                    schema_name='tenant',
                    first_name='Schemas Inc.',
                    last_name='Test',
                    email='test@test.test',
                    active=True,
                    customer_number=102400,
                    valid_until='2018-12-05',
                    on_trial=False)
    tenant.save()


def index(request):
    blogs = Blog.objects.all().order_by('-id')[:2]
    for blog in blogs:
        blog.slugify = slugify(blog.title)
    return render(request, 'Tenants/index.html', {'blogs': blogs})


def check_if_subdomain_available(subdomain):
    existing = InvoiceSite.objects.filter(subdomain=subdomain)
    return existing.count() is 0

class MyDataView(View):
    def get(self, request):
        return render(request, 'user.html', {'form': UserForm()})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username'].lower()
            invoice_site = InvoiceSite.objects.filter(email=email)
            if invoice_site.count() != 0:
                invoice_site = invoice_site[0]
                return redirect('https://' + invoice_site.subdomain + '.invoicegen.nl/inloggen/via-website?email=' + email)
            else:
                return render(request, 'user.html', {'form': form, 'message_error': 'Geen gebruiker gevonden'})
        else:
            return render(request, 'user.html', {'form': form})


class CreateNewInvoiceSite(View):
    def get(self, request):
        return render(request, 'Tenants/registration.html', {'form': InvoiceSiteForm()})

    def post(self, request):
        number_of_users = InvoiceSite.objects.count()
        if number_of_users < 50:
            invoice_site = InvoiceSite()
            f = InvoiceSiteForm(request.POST, instance=invoice_site)
            if f.is_valid() and f.cleaned_data['password'] == f.cleaned_data['password_again']:
                subdomain = slugify(f.cleaned_data['subdomain'].lower())
                email = f.cleaned_data['email'].lower()
                existing_users = InvoiceSite.objects.filter(email=email).count()
                if check_if_subdomain_available(subdomain) and existing_users == 0:
                    create_new_invoice_site(subdomain, user, f)
                    execute_shell_script(subdomain, email, f.cleaned_data['password'], invoice_site.communication_key)
                    return render(request, 'index.html', {'subdomain': subdomain, 'success': 'success'})
                else:
                    return render(request, 'registration.html', {'form': f,
                        "message_error": 'Deze gebruiker of deze bedrijfsnaam bestaat al'})
            else:
                return render('Tenants/registration.html', {'form': f, "error": f.errors})


def create_new_invoice_site(subdomain, user, form):
    user = User.objects.create_user(username=form.cleaned_data['email'],
                                    email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
    invoice_site.user = user
    invoice_site.communication_key = generate_communication_key()
    invoice_site.valid_until = datetime.now() + timedelta(days=31)
    invoice_site.customer_number = 10042000 + InvoiceSite.objects.count() + 1
    invoice_site.subdomain = subdomain
    invoice_site.save()

@csrf_exempt
def get_subscription_status(request):
    if request.method == 'POST':
        invoice_site = InvoiceSite.objects.filter(communication_key=request.POST['key'])
        if invoice_site.count() != 0:
            invoice_site = invoice_site[0]
            return JsonResponse({'first_name': invoice_site.first_name, 'last_name': invoice_site.last_name,
                                 'email': invoice_site.email, 'subdomain': invoice_site.subdomain,
                                 'subscription': invoice_site.active,
                                 'customer_number': invoice_site.customer_number,
                                 'valid_until': get_formatted_string_date_time(invoice_site.valid_until)})
        return JsonResponse({'error': True})


def get_formatted_string_date_time(date):
    return date.strftime("%d-%m-%Y %H:%M:%S")
