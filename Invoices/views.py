from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from Invoices.forms import *
from datetime import date
from django.http import HttpResponse
import datetime
import FactuurMaker
# Create your views here.

@login_required
def get_invoices(request):
    invoices = {}
    yearList = []
    years = Invoice.objects.values("date_created").distinct()
    for dict in years:
        year = dict['date_created'].year
        if year not in yearList:
            yearList.append(year)
            invoices[year] = Invoice.objects.filter(date_created__contains=year)
    toast = None
    if request.session.get('toast'):
        toast = request.session.get('toast')
        del request.session['toast']

    for year in yearList:
        for invoice_obj in invoices[year]:
            products = Product.objects.filter(invoice=invoice_obj)
            invoice_obj.product_set = []
            for product in products:
                invoice_obj.product_set.append(product)

    currentYear = date.today().year
    return render(request, 'invoice_table.html',
                  {'invoices': invoices, 'toast': toast, 'years': yearList, 'currentYear': currentYear})


@login_required
def add_invoice(request):
    context = RequestContext(request)
    if request.method == 'GET':
        invoice = Invoice()
        f = InvoiceForm(instance=invoice)

        return render_to_response('new_edit_invoice.html',
                                  {'form': f, 'invoceid': invoice.id, 'edit': False}, context)
    elif request.method == 'POST':
        invoice = Invoice()
        f = InvoiceForm(request.POST, instance=invoice)

        if f.is_valid():
            f.save(commit=False)
            invoice.date_created = datetime.datetime.now()

            invoice.total_amount = 0
            articles =  f.cleaned_data['articles']
            for article in articles:
                invoice.total_amount += article.price_per_quantity * article.quantity
                invoice.to_company = article.from_company

            with_tax_rate = articles[0].tax_rate != 0
            invoice.contents = FactuurMaker.markdown_generator.create_markdown_file(UserSetting.objects.first(),
                                                                                    articles[0].from_company, get_today_string(),
                                                                                    articles,
                                                                                    f.cleaned_data['invoice_number'], with_tax_rate)
            invoice.save()

            request.session['toast'] = 'Factuur aangemaakt'
            return redirect('/facturen')
        else:
            return render_to_response('new_edit_invoice.html',
                                      {'form': f, 'invoceid': invoice.id, 'edit': False,
                                       'toast': "Formulier ongeldig!"}, context)


@login_required
def edit_invoice(request, invoiceid=-1):
    context = RequestContext(request)
    if request.method == 'GET':
        try:
            invoice = Invoice.objects.get(id=invoiceid)
            f = InvoiceForm(instance=invoice)
            articles = Product.objects.filter(invoice=invoice)

            return render_to_response('new_edit_invoice.html',
                                      {'form': f, 'articles': articles, 'invoceid': invoice.id, 'edit': True,
                                       'invoiceid': invoiceid}, context)
        except:
            request.session['toast'] = 'Factuur niet gevonden'
            return redirect('/facturen')
    elif request.method == 'POST':
        invoice = Invoice.objects.get(id=invoiceid)
        f = InvoiceForm(request.POST, instance=invoice)
        articles = Product.objects.filter(invoice=invoice)

        if f.is_valid():
            f.save()
            request.session['toast'] = 'Factuur gewijzigd'
            return redirect('/facturen')
        else:
            print(f.errors)
            return render_to_response('new_edit_invoice.html',
                                      {'form': f, 'articles': articles, 'invoceid': invoice.id, 'edit': True,
                                       'invoiceid': invoiceid, 'toast': "Formulier ongeldig!"}, context)


@login_required
def delete_invoice(request, invoiceid=-1):
    try:
        invoice = Invoice.objects.get(id=invoiceid)
        articles = Product.objects.filter(invoice=invoice)
        for article in articles:
            article.invoice = None
            article.save()

        invoice.delete()
        request.session['toast'] = 'Verwijderen factuur gelukt'
        return redirect('/facturen')
    except:
        request.session['toast'] = 'Verwijderen factuur mislukt'
        return redirect('/facturen')


@login_required
def generate_invoice(request):
    if request.method == 'POST':
        articles = []
        totaalbedrag = 0
        invoice = Invoice()
        for articleId in request.POST.getlist('articles[]'):
            article = Product.objects.get(id=articleId)
            articles.append(article)
            totaalbedrag += article.quantity * article.price_per_quantity

        today = get_today_string()
        volgnummer = request.POST.get('volgnummer')
        # create invoice and save it
        with_tax_rate = articles[0].tax_rate != 0
        invoice.contents = FactuurMaker.markdown_generator.create_markdown_file(UserSetting.objects.first(),
                                                                    articles[0].from_company, today, articles,
                                                                    volgnummer, with_tax_rate)
        invoice.date_created = datetime.date.today()
        invoice.title = "Factuur " + str(today)
        invoice.to_company = articles[0].from_company
        invoice.invoice_number = volgnummer
        invoice.total_amount = totaalbedrag
        invoice.save()

        for article in articles:
            article.invoice = invoice
            article.save()
    return redirect('/')

def get_today_string():
    today = datetime.date.today()
    today = today.strftime("%d-%m-%Y")
    return today