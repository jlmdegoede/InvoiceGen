from django.shortcuts import render
from Magazine.models import *
# Create your views here.


def magazines(request):
    magazines = Magazine.objects.all()
    return render(request, 'FactuurMaker/magazines.html',
                  {'magazines': magazines})


def add_magazine(request):
    return render(request, 'FactuurMaker/magazines.html',
                  {'magazines': magazines})