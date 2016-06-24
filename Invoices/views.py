from datetime import date
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import *

import Utils.markdown_generator
from InvoiceGen.settings import BASE_DIR
from Invoices.forms import *
from Settings.models import UserSetting
from Utils.date_helper import *
from Utils.docx_generation import *
from Utils.pdf_generation import *
from .models import *


# Create your views here.


@login_required
def get_outgoing_invoices(request):
    dict = get_invoices('outgoing')

    toast = None
    if request.session.get('toast'):
        toast = request.session.get('toast')
        del request.session['toast']

    dict['toast'] = toast
    return render(request, 'outgoing_invoice_table.html', dict)


@login_required
def get_incoming_invoices(request):
    dict = get_invoices('incoming')

    toast = None
    if request.session.get('toast'):
        toast = request.session.get('toast')
        del request.session['toast']

    dict['toast'] = toast
    return render(request, 'incoming_invoice_table.html', dict)


def get_invoices(invoice_objects):
    invoices = {}
    yearList = []
    if invoice_objects == 'outgoing':
        years = OutgoingInvoice.objects.values("date_created").distinct()
        objects = OutgoingInvoice.objects.all()
    else:
        years = IncomingInvoice.objects.values("date_created").distinct()
        objects = IncomingInvoice.objects.all()

    for dict in years:
        year = dict['date_created'].year
        if year not in yearList:
            yearList.append(year)
            invoices[year] = objects.filter(date_created__contains=year)

    for year in yearList:
        if invoice_objects == 'outgoing':
            for invoice_obj in invoices[year]:
                products = Product.objects.filter(invoice=invoice_obj)
                invoice_obj.products = products

    currentYear = date.today().year
    return {'invoices': invoices,  'years': yearList, 'currentYear': currentYear}


@login_required
def add_outgoing_invoice(request):
    context = RequestContext(request)
    if request.method == 'GET':
        invoice = OutgoingInvoice()
        f = OutgoingInvoiceForm(instance=invoice)

        return render_to_response('new_edit_outgoing_invoice.html',
                                  {'form': f, 'invoceid': invoice.id, 'edit': False}, context)
    elif request.method == 'POST':
        invoice = OutgoingInvoice()
        f = OutgoingInvoiceForm(request.POST, instance=invoice)

        if f.is_valid():
            f.save(commit=False)
            invoice.date_created = datetime.datetime.now()
            invoice.total_amount = 0

            products = f.cleaned_data['products']
            for product in products:
                invoice.total_amount += product.price_per_quantity * product.quantity
                invoice.to_company = product.from_company

            invoice.invoice_number = f.cleaned_data['invoice_number']
            invoice.save()

            for product in products:
                product.invoice = invoice
                product.save()
            invoice.save()

            request.session['toast'] = 'Factuur aangemaakt'
            return redirect('/facturen')
        else:
            return render_to_response('new_edit_outgoing_invoice.html',
                                      {'form': f, 'invoceid': invoice.id, 'edit': False,
                                       'toast': "Formulier ongeldig!"}, context)


@login_required
def add_incoming_invoice(request):
    context = RequestContext(request)
    if request.method == 'GET':
        invoice = IncomingInvoice()
        f = IncomingInvoiceForm(instance=invoice)

        return render_to_response('new_edit_incoming_invoice.html',
                                  {'form': f, 'invoceid': invoice.id, 'edit': False}, context)
    elif request.method == 'POST':
        invoice = IncomingInvoice()
        f = IncomingInvoiceForm(request.POST, request.FILES, instance=invoice)

        if f.is_valid():
            f.save(commit=False)
            invoice.date_created = datetime.datetime.now()
            if 'invoice_file' in request.FILES:
                invoice.invoice_file = request.FILES['invoice_file']
            invoice.save()
            request.session['toast'] = 'Factuur aangemaakt'
            return redirect('/facturen/inkomend')
        else:
            return render_to_response('new_edit_incoming_invoice.html',
                                      {'form': f, 'invoceid': invoice.id, 'edit': False,
                                       'toast': "Formulier ongeldig!"}, context)


@login_required
def detail_incoming_invoice(request, invoice_id):
    invoice = IncomingInvoice.objects.get(id=invoice_id)
    print(invoice)
    return render(request, 'view_incoming_invoice.html', {'invoice': invoice})


@login_required
def detail_outgoing_invoice(request, invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    return render(request, 'view_outgoing_invoice.html', {'invoice': invoice})


@login_required
def get_invoice_pdf(request, invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    products = Product.objects.filter(invoice=invoice)
    user = UserSetting.objects.first()
    generate_pdf(products, user, invoice)
    response = HttpResponse(open(BASE_DIR + "/InvoiceTemplates/MaterialDesign/temp/main.pdf", 'rb').read())
    response['Content-Disposition'] = 'attachment; filename=' + invoice.title + '.pdf'
    return response


@login_required
def get_invoice_markdown(request, invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    products = Product.objects.filter(invoice=invoice)
    with_tax_rate = products[0].tax_rate != 0
    contents = Utils.markdown_generator.create_markdown_file(invoice, UserSetting.objects.first(),
                                                             products[0].from_company,
                                                             get_today_string(),
                                                             products,
                                                             with_tax_rate)


    response = HttpResponse(contents, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=invoice' + str(invoice.date_created) + '.md'
    return response

@login_required
def get_invoice_docx(request, invoice_id):
    invoice = OutgoingInvoice.objects.get(id=invoice_id)
    products = Product.objects.filter(invoice=invoice)
    user = UserSetting.objects.first()
    doc = generate_docx_invoice(invoice, user, products, products[0].tax_rate != 0)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    doc.save(response)
    response['Content-Disposition'] = 'attachment; filename=' + invoice.title + '.docx'
    return response


@login_required
def edit_outgoing_invoice(request, invoiceid=-1):
    context = RequestContext(request)
    if request.method == 'GET':
        try:
            invoice = OutgoingInvoice.objects.get(id=invoiceid)
            f = OutgoingInvoiceForm(instance=invoice)
            products = Product.objects.filter(invoice=invoice)

            return render_to_response('new_edit_outgoing_invoice.html',
                                      {'form': f, 'articles': products, 'invoceid': invoice.id, 'edit': True,
                                       'invoiceid': invoiceid}, context)
        except:
            request.session['toast'] = 'Factuur niet gevonden'
            return redirect('/facturen')
    elif request.method == 'POST':
        invoice = Invoice.objects.get(id=invoiceid)
        f = OutgoingInvoiceForm(request.POST, instance=invoice)
        products = Product.objects.filter(invoice=invoice)

        if f.is_valid():
            f.save()
            request.session['toast'] = 'Factuur gewijzigd'
            return redirect('/facturen')
        else:
            return render_to_response('new_edit_outgoing_invoice.html',
                                      {'form': f, 'articles': products, 'invoceid': invoice.id, 'edit': True,
                                       'toast': "Formulier ongeldig!"}, context)


@login_required
def edit_incoming_invoice(request, invoiceid=-1):
    context = RequestContext(request)
    if request.method == 'GET':
        try:
            invoice = IncomingInvoice.objects.get(id=invoiceid)
            f = IncomingInvoiceForm(instance=invoice)

            return render_to_response('new_edit_incoming_invoice.html',
                                      {'form': f, 'invoice': invoice, 'edit': True}, context)
        except:
            request.session['toast'] = 'Factuur niet gevonden'
            return redirect('/facturen/inkomend')
    elif request.method == 'POST':
        invoice = IncomingInvoice.objects.get(id=invoiceid)
        f = IncomingInvoiceForm(request.POST, request.FILES, instance=invoice)

        if f.is_valid():
            f.save(commit=False)
            if 'invoice_file' in request.FILES:
                invoice.invoice_file = request.FILES['invoice_file']
            request.session['toast'] = 'Factuur gewijzigd'
            return redirect('/facturen/inkomend')
        else:
            return render_to_response('new_edit_incoming_invoice.html',
                                      {'form': f, 'invoceid': invoice.id, 'edit': True,
                                       'toast': "Formulier ongeldig!"}, context)


@login_required
def delete_outgoing_invoice(request, invoiceid=-1):
    try:
        invoice = OutgoingInvoice.objects.get(id=invoiceid)
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
def delete_incoming_invoice(request, invoiceid=-1):
    try:
        invoice = IncomingInvoice.objects.get(id=invoiceid)
        invoice.delete()
        request.session['toast'] = 'Verwijderen factuur gelukt'
        return redirect('/facturen/inkomend')
    except:
        request.session['toast'] = 'Verwijderen factuur mislukt'
        return redirect('/facturen/inkomend')


@login_required
def generate_invoice(request):
    if request.method == 'POST':
        articles = []
        totaalbedrag = 0
        invoice = OutgoingInvoice()
        for articleId in request.POST.getlist('articles[]'):
            article = Product.objects.get(id=articleId)
            articles.append(article)
            totaalbedrag += article.quantity * article.price_per_quantity

        today = get_today_string()
        volgnummer = request.POST.get('volgnummer')
        invoice.invoice_number = volgnummer
        # create invoice and save it
        with_tax_rate = articles[0].tax_rate != 0
        invoice.date_created = datetime.date.today()
        invoice.title = "Factuur " + str(today)
        invoice.to_company = articles[0].from_company
        invoice.total_amount = totaalbedrag
        invoice.expiration_date = datetime.datetime.now() + timedelta(days=14)
        invoice.save()

        for article in articles:
            article.invoice = invoice
            article.save()
    return redirect('/')
