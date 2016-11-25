from django.shortcuts import render
from Companies.models import *
from django.shortcuts import *
from Companies.forms import *
from Orders.models import Product
from django.contrib.auth.decorators import login_required
from .tables import CompanyTable
from django_tables2 import RequestConfig

@login_required
def index(request):
    companies = Company.objects.all()
    for company in companies:
        products = Product.objects.filter(from_company=company)
        if products.count() is not 0:
            company.recent_products = products[:3]
    company_table = CompanyTable(companies)
    RequestConfig(request).configure(company_table)
    return render(request, 'Companies/index_companies.html', {'companies': companies, 'company_table': company_table, 'toast': toast})


@login_required
def add_company(request):
    if request.method == 'POST':
        company = Company()
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company.save()
            return redirect(to=index)
        else:
            return render(request, 'Companies/new_edit_company.html', {'form': form, 'error': form.errors})
    else:
        company_form = CompanyForm()
        return render(request, 'Companies/new_edit_company.html', {'form': company_form})


@login_required
def edit_company(request, company_id):
    if request.method == 'GET':
        try:
            company = Company.objects.get(id=company_id)
            form = CompanyForm(instance=company)
            return render(request, 'Companies/new_edit_company.html', {'form': form, 'edit': True, 'company_id': company.id})
        except:
            return redirect(to=index)
    elif request.method == 'POST':
        company = Company.objects.get(id=company_id)
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company.save()
            return redirect(to=index)
        else:
            return render(request, 'Companies/new_edit_company.html', {'form': form, 'error': form.errors, 'company_id': company.id})


@login_required
def delete_company(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
        products = Product.objects.filter(from_company=company).count()
        if products == 0:
            company.delete()
            request.session['toast'] = 'Opdrachtgever verwijderd'
            return redirect('/opdrachtgevers')
        else:
            request.session['toast'] = 'Opdrachtgever niet verwijderd: nog opdrachten gekoppeld'
            return redirect('/opdrachtgevers')
    except:
            request.session['toast'] = 'Opdrachtgever niet verwijderd'
            return redirect('/opdrachtgevers')
