from django.shortcuts import render, redirect
from InvoiceGen.site_settings import ALLOWED_HOSTS
import string
import random
from Todo.models import *
# Create your views here.
REDIRECT_URI = 'https://' + ALLOWED_HOSTS[0] + '/'


def index(request):
    state = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(25))
    url = 'https://invoicegen.nl/wunderlist?origin=' + REDIRECT_URI
    todo = TodoAuth()
    todo.state = state
    todo.user_id = request.user
    todo.save()
    return render(request, 'todo.html', {'url': url, 'state': state})


def save_auth_token(request):
    if request.method == 'GET':
        state = request.GET['state']
        code = request.GET['code']
        auth_token = request.GET['auth_token']
        todo = TodoAuth.Objects.filter(user_id=request.user, active=True)
        if state == todo.state:
            todo.auth_token = auth_token
            todo.save()
        return redirect(to='/')

