from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from FactuurMaker.models import Article
from django.contrib.auth import authenticate
from RestApi.models import *
from datetime import date
import django.utils.crypto
from FactuurMaker.views import get_yearly_stats
# Create your views here.

@csrf_exempt
def get_json_article_list(request):
    if check_session_id(request.POST["session_id"]):
        title_list = map(Article.serialize, Article.objects.all())
        return JsonResponse(list(title_list), content_type="application/json", safe=False)
    return JsonResponse({"error": "Invalid session ID supplied"}, content_type="application/json", safe=False)


@csrf_exempt
def get_json_article(request, article_id):
    if check_session_id(request.POST["session_id"]):
        article = map(Article.serialize, Article.objects.filter(id=article_id))
        return JsonResponse(list(article), content_type="application/json", safe=False)
    return JsonResponse({"error": "Invalid session ID supplied"}, content_type="application/json", safe=False)


@csrf_exempt
def save_json_article(request):
    for json_values in request.POST:
        data = json.loads(json_values)
        if check_session_id(data["session_id"]):
            article_id = data['server_id']
            if (article_id != -1):
                article = Article.objects.get(id=article_id)
            else:
                article = Article()

            article.title = data["title"]
            article.briefing = data["briefing"]
            article.word_count = data["wordcount"]
            article.done = data["done"]
            article.date_deadline = data["deadline"]
            article.magazine = data["magazine"]
            article.magazine_number = data["magazine_nr"]
            article.date_received = data["date_received"]
            article.save()
            return JsonResponse({"success": True}, content_type="application/json", safe=False)
        return JsonResponse({"error": "Invalid session ID supplied"}, content_type="application/json", safe=False)


@csrf_exempt
def get_session_id(request):
    for json_values in request.POST:
        data = json.loads(json_values)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        returnvalues = None
        if user is not None:
            session_id = SessionIDs.objects.filter(user=user)
            if session_id.exists():
                returnvalues = list(session_id)[0].serialize()
            else:
                session_id = SessionIDs()
                session_id.date_created = date.today()
                session_id.device = data['device']
                session_id.last_known_ip = data['ip']
                session_id.software_version = data['software_version']
                session_id.valid = True
                session_id.user = user
                session_id.session_id = django.utils.crypto.get_random_string(length=30, allowed_chars='abcdefghijklmnopqrstuvwxyz123456789!@')
                session_id.save()
                returnvalues = session_id.serialize()

    return JsonResponse(returnvalues, content_type="application/json", safe=False)

@csrf_exempt
def check_session_id(p_session_id):
    try:
        session_id = SessionIDs.objects.get(session_id=p_session_id)
        if session_id is not None:
            return True
    except:
        return False

@csrf_exempt
def view_statistics(request):
    if check_session_id(request.POST["session_id"]):
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
        return JsonResponse(totale_inkomsten, content_type="application/json", safe=False)

    return JsonResponse({"error": "Invalid session ID supplied"}, content_type="application/json", safe=False)