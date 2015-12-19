from django import forms
from Magazine.models import *


class MagazineForm(forms.ModelForm):
    title = forms.CharField()

    class Meta:
        model = Magazine
        fields = ('title',)

