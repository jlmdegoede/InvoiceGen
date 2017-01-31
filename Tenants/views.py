from django.shortcuts import render
from .models import Client
# Create your views here.

def create_public_tenant(request):
    tenant = Client(domain_url='test3.invoicegen.nl', # don't add your port or www here! on a local server you'll want to use localhost here
                    schema_name='tenant3',
                    name='Schemas Inc.',
                    paid_until='2018-12-05',
                    on_trial=False)
    tenant.save()
    tenant = Client(domain_url='test4.invoicegen.nl', # don't add your port or www here!
                schema_name='tenant4',
                name='jochemdegoede',
                paid_until='2019-12-05',
                on_trial=False)
    tenant.save() # migrate_schemas automatically called, your tenant is ready to be used!
