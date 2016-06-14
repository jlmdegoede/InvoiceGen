from datetime import date

import markdown
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import *

from Agreements.models import Agreement
from Companies.forms import CompanyForm
from Companies.models import Company
from Orders.forms import *
from Utils.search_query import get_query
from Todo.views import create_task_from_order
from Settings.views import get_setting
import asyncio
import Settings.views


# Create your views here.


@login_required
def index(request):
    articles = {}
    yearList = []
    years = Product.objects.values("date_deadline").distinct()
    for dict in years:
        year = dict['date_deadline'].year
        if year not in yearList:
            yearList.append(year)
            articles[year] = Product.objects.filter(date_deadline__contains=year, done=True)
            for article in articles[year]:
                article.clean_url_title = article.title.replace(' ', '-').lower()
                agreements = Agreement.objects.filter(article_concerned=article)
                if agreements.count() != 0:
                    article.agreement = agreements[0]
    toast = None
    if request.session.get('toast'):
        toast = request.session.get('toast')
        del request.session['toast']

    yearList.sort(reverse=True)
    active_articles = Product.objects.filter(done=False)
    currentYear = date.today().year
    no_settings = Settings.views.no_settings_created_yet()
    return render(request, 'index.html',
                  {'articles': articles, 'active_articles': active_articles, 'toast': toast, 'years': yearList,
                   'currentYear': currentYear, 'first_time': no_settings})


@login_required
def view_article(request, articleid):
    try:
        article = Product.objects.get(id=articleid)
        if Agreement.objects.filter(article_concerned=article).count() != 0:
            article.agreement = Agreement.objects.filter(article_concerned=article)[0]
        return render(request, 'view_article.html', {'article': article})
    except Exception as err:
        print(err)
        request.session['toast'] = 'Product niet gevonden'
        return redirect('/')

@login_required
def mark_products_as_done(request):
    if request.method == 'POST':
        products = []
        for productId in request.POST.getlist('products[]'):
            product = Product.objects.get(id=productId)
            product.done = True
            product.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


@login_required
def view_statistics(request):
    year = date.today().year
    year_list = [int(year) - 5, int(year) - 4, int(year) - 3, int(year) - 2, int(year) - 1, int(year)]
    nr_of_articles = []
    not_yet_invoiced = []
    nr_of_words = []
    totale_inkomsten = []
    for i in range(int(year) - 5, int(year) + 1):
        tuple = get_yearly_stats(i)
        nr_of_articles.append(tuple[0])
        nr_of_words.append(tuple[1])
        totale_inkomsten.append(tuple[2])
        not_yet_invoiced.append(tuple[3])
    return render(request, 'statistics.html',
                  {'nr_of_articles': nr_of_articles, 'not_yet_invoiced': not_yet_invoiced, 'nr_of_words': nr_of_words,
                   'totale_inkomsten': totale_inkomsten, 'year': year, 'year_list': year_list})


def get_yearly_stats(year):
    print(year)
    nr_of_articles = 0
    totale_inkomsten = 0
    nr_of_words = 0
    all_articles = Product.objects.filter(done=True)
    for article in all_articles:
        if article.date_deadline.year == int(year):
            totale_inkomsten += article.quantity * article.price_per_quantity
            nr_of_words += article.quantity
            nr_of_articles += 1
    not_yet_invoiced = 0
    not_yet_invoiced_articles = Product.objects.filter(done=False)
    for article in not_yet_invoiced_articles:
        not_yet_invoiced += article.quantity * article.price_per_quantity

    return nr_of_articles, nr_of_words, totale_inkomsten, not_yet_invoiced


@login_required
def add_company_inline(request):
    context = RequestContext(request)
    if request.method == 'POST':
        company = Company()
        f = CompanyForm(request.POST, instance=company)
        if f.is_valid():
            company.save()
            request.session['toast'] = 'Bedrijf toegevoegd'
            return JsonResponse({'company_id': company.id, 'company_name': company.company_name})
    if request.method == 'GET':
        form = CompanyForm()
        return render_to_response('new_company_inline.html', {'form': form}, context)


@login_required
def add_article(request):
    context = RequestContext(request)
    if request.method == 'POST':
        article = Product()
        f = ProductForm(request.POST, instance=article)
        article.invoice = None
        if f.is_valid():
            article.save()
            request.session['toast'] = 'Opdracht toegevoegd'
            if get_setting('auto_wunderlist', False):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(create_task_from_order(article))
                loop.close()
            return redirect('/')
        else:
            return render_to_response('new_edit_article.html',
                                      {'toast': 'Formulier onjuist ingevuld', 'form': f, 'error': f.errors}, context)
    else:
        form = ProductForm()

        return render_to_response('new_edit_article.html', {'form': form}, context)


@login_required
def download_markdown(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    response = HttpResponse(invoice.contents, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=invoice' + str(invoice.date_created) + '.md'
    return response


@login_required
def edit_article(request, articleid=-1):
    context = RequestContext(request)
    if request.method == 'GET':
        try:
            article = Product.objects.get(id=articleid)
            f = ProductForm(instance=article)

            return render_to_response('new_edit_article.html',
                                      {'form': f, 'edit': True, 'articleid': articleid}, context)
        except:
            request.session['toast'] = 'Opdracht niet gevonden'
            return redirect('/')
    elif request.method == 'POST':
        article = Product.objects.get(id=articleid)
        f = ProductForm(request.POST, instance=article)

        if f.is_valid():
            f.save()
            request.session['toast'] = 'Opdracht gewijzigd'
            return redirect('/')
        else:
            return render_to_response('new_edit_article.html',
                                      {'form': f, 'edit': True, 'articleid': articleid, 'toast': 'Ongeldig formulier'},
                                      context)


@login_required
def delete_article(request, articleid=-1):
    try:
        article_to_delete = Product.objects.get(id=articleid)
        article_to_delete.delete()
        request.session['toast'] = 'Opdracht verwijderd'
        return redirect('/')
    except:
        request.session['toast'] = 'Verwijderen mislukt'
        return redirect('/')


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')


def user_login(request):
    context = RequestContext(request)
    form = UserForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            return render_to_response('login.html', {'error': "Ongeldige inloggegevens", 'form': form}, context)
    else:
        return render_to_response('login.html', {'form': form}, context)


@login_required
def search(request):
    query_string = ''
    found_products = None
    found_agreements = None
    found_invoices = None
    found_companies = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        product_query = get_query(query_string, ['title', 'briefing'])
        agreement_query = get_query(query_string, ['agreement_text_copy', 'client_name', 'client_emailaddress', ])
        invoice_query = get_query(query_string, ['title', 'contents', ])
        companies_query = get_query(query_string, ['company_name', 'company_address', 'company_city_and_zipcode'])

        found_products = Product.objects.filter(product_query).order_by('-date_received')
        found_agreements = Agreement.objects.filter(agreement_query).order_by('-created')
        found_invoices = Invoice.objects.filter(invoice_query).order_by('-date_created')
        found_companies = Company.objects.filter(companies_query)

    return render_to_response('search_results.html',
                              {'query_string': query_string, 'found_products': found_products,
                               'found_agreements': found_agreements, 'found_invoices': found_invoices,
                               'found_companies': found_companies},
                              context_instance=RequestContext(request))
