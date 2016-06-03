from django.shortcuts import render
from Company.models import *
from django.shortcuts import *
from Company.forms import *
from FactuurMaker.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    context = RequestContext(request)
    companies = Company.objects.all()
    for company in companies:
        products = Product.objects.filter(from_company=company)
        if products.count() is not 0:
            company.recent_products = products[:3]

    toast = None
    if request.session.get('toast'):
        toast = request.session.get('toast')
        del request.session['toast']
    return render_to_response('index.html', {'companies': companies, 'toast': toast}, context)


@login_required
def add_company(request):
    context = RequestContext(request)
    if request.method == 'POST':
        company = Company()
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company.save()
            return redirect(to=index)
        else:
            return render_to_response('new_edit_company.html', {'form': form, 'error': form.errors}, context)
    else:
        company_form = CompanyForm()
        return render_to_response('new_edit_company.html', {'form': company_form}, context)


@login_required
def edit_company(request, company_id):
    context = RequestContext(request)
    if request.method == 'GET':
        try:
            company = Company.objects.get(id=company_id)
            form = CompanyForm(instance=company)
            return render_to_response('new_edit_company.html', {'form': form, 'edit': True, 'company_id': company.id}, context)
        except:
            return redirect(to=index)
    elif request.method == 'POST':
        company = Company.objects.get(id=company_id)
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company.save()
            return redirect(to=index)
        else:
            return render_to_response('new_edit_company.html', {'form': form, 'error': form.errors, 'company_id': company.id}, context)


@login_required
def delete_company(request, company_id):
    context = RequestContext(request)
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
