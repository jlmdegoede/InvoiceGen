from django.shortcuts import *
from Magazine.forms import *
from django.forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def magazines(request):
    magazines = Magazine.objects.all()
    for magazine in magazines:
        uitgave = MagazineUitgave.objects.filter(magazine=magazine.id)
        if uitgave:
            magazine.volgende = uitgave.latest('verschijningsdatum')
    return render(request, 'magazines.html',
                  {'magazines': magazines})


@login_required
def add_magazine(request):
    if request.method == 'POST':
        magazine = Magazine()
        f = MagazineForm(request.POST, instance=magazine)
        if f.is_valid():
            magazine.save()
            request.session['toast'] = 'Magazine toegevoegd'
            return redirect('/magazines')
    else:
        magazine = MagazineForm()

        return render(request, 'new_edit_magazine.html',
                  {'magazine': magazine})


@login_required
def edit_magazine(request, magazine_id):
    if request.method == 'POST':
        magazine = Magazine.objects.get(id=magazine_id)
        f = MagazineForm(request.POST, instance=magazine)
        if f.is_valid():
            magazine.save()
            request.session['toast'] = 'Magazine toegevoegd'
            return redirect('/magazines')
    else:
        instance_mag = Magazine.objects.get(id=magazine_id)
        magazine = MagazineForm(instance=instance_mag)

        return render(request, 'new_edit_magazine.html',
                  {'magazine': magazine, 'edit': True, 'magazine_id': instance_mag.id})


@login_required
def add_magazine_uitgave(request, magazine_id):
    MagazineUitgaveFormset = inlineformset_factory(Magazine, MagazineUitgave, fields=('nummer','verschijningsdatum'),
                                                   form=MagazineUitgaveForm)
    instance_mag = Magazine.objects.get(id=magazine_id)
    if request.method == 'POST':
        f = MagazineUitgaveFormset(request.POST, instance=instance_mag)
        if f.is_valid():
            f.save()
            request.session['toast'] = 'Magazine-uitgaves toegevoegd'
            return redirect('/magazines')
        else:

            return render(request, 'new_magazineuitgaves.html',
                  {'magazine_uitgave_form': f, 'edit': True, 'magazine_id': instance_mag.id})
    else:
        MagazineUitgaveFormset(instance=instance_mag)

        return render(request, 'new_magazineuitgaves.html',
                  {'magazine_uitgave_form': MagazineUitgaveFormset, 'edit': True, 'magazine_id': instance_mag.id})

@login_required
def view_magazine_uitgaves(request, magazine_id):
    magazine_uitgaves = MagazineUitgave.objects.filter(magazine=magazine_id)
    magazine = Magazine.objects.get(id=magazine_id)

    return render(request, 'view_magazine_uitgaves.html',
                  {'magazine_uitgaves': magazine_uitgaves, 'edit': True, 'magazine': magazine})