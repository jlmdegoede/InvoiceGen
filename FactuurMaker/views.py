from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from FactuurMaker.forms import *
from datetime import date
import datetime
import markdown
from django.http import HttpResponse
# Create your views here.

@login_required
def index(request):
    articles = {}
    yearList = []
    years = Article.objects.values("date_deadline").distinct()
    for dict in years:
        year = dict['date_deadline'].year
        if year not in yearList:
            yearList.append(year)
            articles[year] = Article.objects.filter(date_deadline__contains=year, done=True)
            for article in articles[year]:
                if article.paid == False:
                    article.paid = 'Nee'
                else:
                    article.paid = 'Ja'
                article.clean_url_title = article.title.replace(' ', '-').lower()
    toast = None
    if request.session.get('toast'):
        toast = request.session.get('toast')
        del request.session['toast']

    yearList.sort(reverse=True)
    active_articles = Article.objects.filter(done=False)
    currentYear = date.today().year
    return render(request, 'FactuurMaker/index.html',
                  {'articles': articles, 'active_articles': active_articles, 'toast': toast, 'years': yearList,
                   'currentYear': currentYear})


@login_required
def view_article(request, articleid):
    try:
        article = Article.objects.get(id=articleid)
        if article.paid == False:
            article.paid = 'Nee'
        else:
            article.paid = 'Ja'
        return render(request, 'FactuurMaker/view_article.html', {'article': article})
    except:
        request.session['toast'] = 'Artikel niet gevonden'
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
    all_articles = Article.objects.filter(done=True)
    for article in all_articles:
        if (article.date_deadline.year == int(year)):
            totale_inkomsten += article.word_count * 0.25
            nr_of_words += article.word_count
            nr_of_articles += 1
    not_yet_invoiced = 0
    not_yet_invoiced_articles = Article.objects.filter(done=False)
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
def add_article(request):
    context = RequestContext(request)
    if request.method == 'POST':
        article = Article()
        f = ArticleForm(request.POST, instance=article)
        article.invoice = None
        if f.is_valid():
            article.save()
            request.session['toast'] = 'Artikel toegevoegd'
            return redirect('/')
        else:
            return render_to_response('FactuurMaker/new_edit_article.html',
                                      {'toast': 'Formulier onjuist ingevuld', 'form': f, 'error': f.errors}, context)
    else:
        form = ArticleForm()

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
            article = Article.objects.get(id=articleid)
            f = ArticleForm(instance=article)

            return render_to_response('FactuurMaker/new_edit_article.html',
                                      {'form': f, 'edit': True, 'articleid': articleid}, context)
        except:
            request.session['toast'] = 'Artikel niet gevonden'
            return redirect('/')
    elif request.method == 'POST':
        article = Article.objects.get(id=articleid)
        f = ArticleForm(request.POST, instance=article)

        if f.is_valid():
            f.save()
            request.session['toast'] = 'Artikel gewijzigd'
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
            articles = Article.objects.filter(invoice=invoice)

            return render_to_response('FactuurMaker/new_edit_invoice.html',
                                      {'form': f, 'articles': articles, 'invoceid': invoice.id, 'edit': True,
                                       'invoiceid': invoiceid}, context)
        except:
            request.session['toast'] = 'Factuur niet gevonden'
            return redirect('/invoices')
    elif request.method == 'POST':
        invoice = Invoice.objects.get(id=invoiceid)
        f = InvoiceForm(request.POST, instance=invoice)
        articles = Article.objects.filter(invoice=invoice)

        if f.is_valid():
            f.save()
            request.session['toast'] = 'Factuur gewijzigd'
            return redirect('/invoices')
        else:
            return render_to_response('FactuurMaker/new_edit_invoice.html',
                                      {'form': f, 'articles': articles, 'invoceid': invoice.id, 'edit': True,
                                       'invoiceid': invoiceid, 'toast': "Formulier ongeldig!"}, context)


@login_required
def add_article_to_invoice(request):
    print(request)
    if request.method == 'POST':
        invoice = Invoice.objects.get(id=request.POST.get('invoiceid'))
        article = Article.objects.get(title=request.POST.get('article'))
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
        article = Article.objects.get(id=request.POST.get('articleid'))
        if article.invoice == invoice:
            article.invoice = None
            article.save()
            return HttpResponse("success")
        else:
            return HttpResponse("fail")


@login_required
def delete_article(request, articleid=-1):
    try:
        article_to_delete = Article.objects.get(id=articleid)
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
        articles = Article.objects.filter(invoice=invoice)
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
            article = Article.objects.get(id=articleId)
            articles.append(article)
            totaalbedrag += article.word_count * article.word_price

        today = datetime.date.today()
        today = today.strftime("%d-%m-%Y")
        volgnummer = request.POST.get('volgnummer')
        # create invoice and save it
        invoice.contents = markdown_generator.create_markdown_file(UserSetting.objects.get(naam='Jochem de Goede'),
                                                                   CompanySetting.objects.get(
                                                                       bedrijfsnaam='Reshift Digital'), today, articles,
                                                                   volgnummer)
        invoice.date_created = datetime.date.today()
        invoice.from_address = "jochem@degoede.email"
        invoice.to_address = "factuur@reshift.nl"
        invoice.invoice_number = volgnummer
        invoice.total_amount = totaalbedrag
        invoice.save()

        for article in articles:
            article.invoice = invoice
            invoice.article_set.add(article)
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
            print("Ongeldige inloggegevens: {0}, {1}".format(username, password))
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
        try:
            company = CompanySetting.objects.get(id=1)
        except:
            company = CompanySetting()
        user.naam = request.POST['naam']
        user.emailadres = request.POST['emailadres']
        user.woonplaats = request.POST['woonplaats']
        user.adres = request.POST['adres']
        user.iban = request.POST['iban']
        user.save()

        company.bedrijfsplaats = request.POST['bedrijfsplaats']
        company.bedrijfsadres = request.POST['bedrijfsadres']
        company.bedrijfsnaam = request.POST['bedrijfsnaam']
        company.save()

        toast = 'Instellingen opgeslagen'
    user_i = UserSetting.objects.all().first()
    company_i = CompanySetting.objects.first()
    if not user_i:
        user_i = UserSetting()
    if not company_i:
        company_i = CompanySetting()
    user = UserSettingForm(instance=user_i)
    company = CompanySettingForm(instance=company_i)

    return render(request, 'FactuurMaker/settings.html',
                  {'user': user, 'company': company, 'toast': toast})

