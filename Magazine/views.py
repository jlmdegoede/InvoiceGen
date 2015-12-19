from django.shortcuts import render
from Magazine.models import *
from Magazine.forms import *
from django.forms import inlineformset_factory
# Create your views here.


def magazines(request):
    magazines = Magazine.objects.all()
    return render(request, 'magazines.html',
                  {'magazines': magazines})


def add_magazine(request):
    magazine = MagazineForm()
    magazineFormSet = inlineformset_factory(Magazine, MagazineUitgave, fields=('nummer', 'verschijningsdatum'))

    return render(request, 'new_edit_magazine.html',
                  {'magazine': magazineFormSet})