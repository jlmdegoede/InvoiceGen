from django.shortcuts import render, redirect
from InvoiceGen.site_settings import ALLOWED_HOSTS
import string
import random
from Todo.models import *
import json
from Orders.models import Product
import requests
from django.contrib.auth.decorators import login_required
import Settings.views

# Create your views here.
REDIRECT_URI = 'https://' + ALLOWED_HOSTS[0] + '/'


def get_wunderlist_url(request):
    state = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(25))
    url = 'https://invoicegen.nl/wunderlist/?origin=' + REDIRECT_URI
    todo = TodoAuth()
    todo.state = state
    todo.user_id = request.user
    todo.save()
    return {'url': url, 'state': state}


@login_required
def save_auth_token(request):
    if request.method == 'GET':
        state = request.GET['state']
        code = request.GET['code']
        auth_token = request.GET['auth_token']
        todo = TodoAuth.objects.filter(user_id=request.user, valid=True)[0]
        todo.auth_token = auth_token
        todo.save()
        return redirect(to='/')


def get_lists():
    req = requests.get('https://a.wunderlist.com/api/v1/lists', headers=get_headers())
    return json.loads(req.text)

def create_new_list(title):
    post_data = convert_to_json_utf8({'title': title,})
    req = requests.post('https://a.wunderlist.com/api/v1/lists', post_data, headers=get_headers())
    return json.loads(req.text)


def get_headers():
    return {'X-Access-Token': TodoAuth.objects.first().auth_token, 'X-Client-ID': 'cefa22337f5c32a1713f',
            'Content-Type': 'application/json'}


def convert_to_json_utf8(data):
    return json.dumps(data).encode('utf-8')


async def create_task_from_order(product):
    list_id = Settings.views.get_setting('wunderlist', 0)
    if list_id is not 0:
        title = product.title
        completed = product.done
        due_date = str(product.date_deadline.isoformat())

        post_data = convert_to_json_utf8(
            {'list_id': int(list_id), 'title': title, 'completed': completed, 'due_date': due_date})
        req = requests.post('https://a.wunderlist.com/api/v1/tasks', post_data, headers=get_headers())

        print(req.text)
        return True
    return False
