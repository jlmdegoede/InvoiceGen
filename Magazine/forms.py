from django import forms
from Magazine.models import *


class MagazineForm(forms.ModelForm):
    titel = forms.CharField()

    class Meta:
        model = Magazine
        fields = ('titel',)


class MagazineUitgaveForm(forms.ModelForm):
    verschijningsdatum = forms.DateField(label="Verschijningsdatum", input_formats=['%d-%m-%Y'], widget=forms.widgets.DateInput(format="%d-%m-%Y",attrs={'class':'datepicker'}))

    class Meta:
        model = MagazineUitgave
        fields = ('nummer','verschijningsdatum')

