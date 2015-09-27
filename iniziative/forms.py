# coding=utf-8
__author__ = 'Sig'

from django.forms import ModelForm, Textarea, TextInput
from .models import SottoIniziativa, Raggruppamento
from mongoengine import *


class SottoIniziativaForm():
    """
    Attenzione che il campo iniziativa che è una chiave esterna non lo metto proprio così il form potrà essere
    validato senza errori.
    Dopo la validazione scrivo la chiave esterna e poi lo salvo ma tutto questo lo farò nella view !
    """
    class Meta:
        model = SottoIniziativa
        fields = ['nome', 'descrizione', 'in_uso']
        widgets = {
            'nome': TextInput(attrs={'size': 60}),
            'descrizione': Textarea(attrs={'cols': 40, 'rows': 2}),
        }


class GruppoForm(ModelForm):
    """
    Attenzione che il campo sotto-iniziativa che è una chiave esterna non lo metto proprio così il form potrà essere
    validato senza errori.
    Dopo la validazione scrivo la chiave esterna e poi lo salvo ma tutto questo lo farò nella view !
    """
    class Meta:
        model = Raggruppamento
        fields = ['nome', 'descrizione', 'ordine', 'in_uso']
        widgets = {
            'nome': TextInput(attrs={'size': 60}),
            'descrizione': Textarea(attrs={'cols': 40, 'rows': 2}),
            'ordine': TextInput(attrs={'size': 60}),
        }