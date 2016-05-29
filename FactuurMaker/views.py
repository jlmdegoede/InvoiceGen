from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from FactuurMaker.forms import *
from datetime import date
import datetime
import markdown
from django.http import HttpResponse, JsonResponse
from AgreementModule.models import Agreement
import FactuurMaker.markdown_generator
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
    toast = None
    if request.session.get('toast'):
        toast = request.session.get('toast')
        del request.session['toast']

    yearList.sort(reverse=True)
    active_articles = Product.objects.filter(done=False)
    currentYear = date.today().year
    return render(request, 'FactuurMaker/index.html',
                  {'articles': articles, 'active_articles': active_articles, 'toast': toast, 'years': yearList,
                   'currentYear': currentYear})


@login_required
def view_article(request, articleid):
    try:
        article = Product.objects.get(id=articleid)
        if Agreement.objects.filter(article_concerned=article).count() != 0:
            article.agreement = Agreement.objects.filter(article_concerned=article)[0]
        return render(request, 'FactuurMaker/view_article.html', {'article': article})
    except Exception as err:
        print(err)
        request.session['toast'] = 'Product niet gevonden'
        return redirect('/')


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
    return render(request, 'FactuurMaker/statistics.html',
                  {'nr_of_articles': nr_of_articles, 'not_yet_invoiced': not_yet_invoiced, 'nr_of_words': nr_of_words,
                   'totale_inkomsten': totale_inkomsten, 'year': year, 'year_list': year_list})


def get_yearly_stats(year):
    print(year)
    nr_of_articles = 0
    totale_inkomsten = 0
    nr_of_words = 0
    all_articles = Product.objects.filter(done=True)
    for article in all_articles:
        if (article.date_deadline.year == int(year)):
            totale_inkomsten += article.quantity * article.price_per_quantity
            nr_of_words += article.quantity
            nr_of_articles += 1
    not_yet_invoiced = 0
    not_yet_invoiced_articles = Product.objects.filter(done=False)
    for article in not_yet_invoiced_articles:
        not_yet_invoiced += article.word_count * 0.25

    return (nr_of_articles, nr_of_words, totale_inkomsten, not_yet_invoiced)


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
    return render(request, 'FactuurMaker/invoice_table.html',
                  {'invoices': invoices, 'toast': toast, 'years': yearList, 'currentYear': currentYear})


@login_required
def view_markdown(request, invoice_id):
    # try:
    invoice = Invoice.objects.get(id=invoice_id)
    return render(request, 'FactuurMaker/markdown.html', {'invoice_id': invoice.id,
                                                          'html': markdown.markdown(invoice.contents, extensions=[
                                                              'markdown.extensions.tables',
                                                              'markdown.extensions.nl2br'])})
    # except:
    #    request.session['toast'] = 'Factuur niet gevonden'
    #   return redirect('/invoices')


@login_required
def add_company_inline(request):
    context = RequestContext(request)
    if request.method == 'POST':
        company = Company()
        f = CompanyForm(request.POST, instance=company)
        if f.is_valid():
            company.save()
            request.session['toast'] = 'Bedrijf toegevoegd'
            return JsonResponse({'company_id': company.id, 'company_name': company.bedrijfsnaam})
    if request.method == 'GET':
        form = CompanyForm()
        return render_to_response('FactuurMaker/new_company_inline.html', {'form': form}, context)


@login_required
def add_article(request):
    context = RequestContext(request)
    if request.method == 'POST':
        article = Product()
        f = ProductForm(request.POST, instance=article)
        article.invoice = None
        if f.is_valid():
            article.save()
            request.session['toast'] = 'Artikel toegevoegd'
            return redirect('/')
        else:
            return render_to_response('FactuurMaker/new_edit_article.html',
                                      {'toast': 'Formulier onjuist ingevuld', 'form': f, 'error': f.errors}, context)
    else:
        form = ProductForm()

        return render_to_response('FactuurMaker/new_edit_article.html', {'form': form}, context)


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

            return render_to_response('FactuurMaker/new_edit_article.html',
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
            return render_to_response('FactuurMaker/new_edit_article.html',
                                      {'form': f, 'edit': True, 'articleid': articleid, 'toast': 'Ongeldig formulier'},
                                      context)


@login_required
def add_invoice(request):
    context = RequestContext(request)
    if request.method == 'GET':
        invoice = Invoice()
        f = InvoiceForm(instance=invoice)

        return render_to_response('FactuurMaker/new_edit_invoice.html',
                                  {'form': f, 'invoceid': invoice.id, 'edit': False}, context)
    elif request.method == 'POST':
        invoice = Invoice()
        f = InvoiceForm(request.POST, instance=invoice)

        if f.is_valid():
            f.save()
            request.session['toast'] = 'Factuur aangemaakt'
            return redirect('/invoices')
        else:
            return render_to_response('FactuurMaker/new_edit_invoice.html',
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

            return render_to_response('FactuurMaker/new_edit_invoice.html',
                                      {'form': f, 'articles': articles, 'invoceid': invoice.id, 'edit': True,
                                       'invoiceid': invoiceid}, context)
        except:
            request.session['toast'] = 'Factuur niet gevonden'
            return redirect('/invoices')
    elif request.method == 'POST':
        invoice = Invoice.objects.get(id=invoiceid)
        f = InvoiceForm(request.POST, instance=invoice)
        articles = Product.objects.filter(invoice=invoice)

        if f.is_valid():
            f.save()
            request.session['toast'] = 'Factuur gewijzigd'
            return redirect('/invoices')
        else:
            print(f.errors)
            return render_to_response('FactuurMaker/new_edit_invoice.html',
                                      {'form': f, 'articles': articles, 'invoceid': invoice.id, 'edit': True,
                                       'invoiceid': invoiceid, 'toast': "Formulier ongeldig!"}, context)


@login_required
def add_article_to_invoice(request):
    print(request)
    if request.method == 'POST':
        invoice = Invoice.objects.get(id=request.POST.get('invoiceid'))
        article = Product.objects.get(title=request.POST.get('article'))
        if article.invoice == None:
            article.invoice = invoice
            article.save()
            return HttpResponse("success")
        else:
            return HttpResponse("fail")


@login_required
def delete_article_from_invoice(request):
    if request.method == 'POST':
        invoice = Invoice.objects.get(id=request.POST.get('invoiceid'))
        article = Product.objects.get(id=request.POST.get('articleid'))
        if article.invoice == invoice:
            article.invoice = None
            article.save()
            return HttpResponse("success")
        else:
            return HttpResponse("fail")


@login_required
def delete_article(request, articleid=-1):
    try:
        article_to_delete = Product.objects.get(id=articleid)
        article_to_delete.delete()
        request.session['toast'] = 'Artikel verwijderd'
        return redirect('/')
    except:
        request.session['toast'] = 'Verwijderen mislukt'
        return redirect('/')


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
        return redirect('/invoices')
    except:
        request.session['toast'] = 'Verwijderen factuur mislukt'
        return redirect('/invoices')


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

        today = datetime.date.today()
        today = today.strftime("%d-%m-%Y")
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


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            return render_to_response('FactuurMaker/login.html', {'error': "Ongeldige inloggegevens"}, context)
    else:
        form = UserForm()
        return render_to_response('FactuurMaker/login.html', {'form': form}, context)


@login_required
def settings(request):
    toast = ''
    if request.method == 'POST':
        try:
            user = UserSetting.objects.get(id=1)
        except:
            user = UserSetting()
        user.naam = request.POST['naam']
        user.emailadres = request.POST['emailadres']
        user.plaats_en_postcode = request.POST['plaats_en_postcode']
        user.adres = request.POST['adres']
        user.iban = request.POST['iban']
        user.save()

        toast = 'Instellingen opgeslagen'
    user_i = UserSetting.objects.all().first()
    if not user_i:
        user_i = UserSetting()
    user = UserSettingForm(instance=user_i)

    return render(request, 'FactuurMaker/settings.html',
                  {'user': user, 'toast': toast})

