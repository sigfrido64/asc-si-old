# coding=utf-8
__author__ = 'Sig'


from django import forms
from .models import Iniziativa


class IniziativaForm(forms.ModelForm):
    # name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Iniziativa
        fields = ('iniziativa', 'descrizione', 'cup_cig')


