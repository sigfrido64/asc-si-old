# coding=utf-8
__author__ = 'Sig'

from django.forms import ModelForm
from .models import Iniziativa, SottoIniziativa, Raggruppamento


class IniziativaMixin(object):
    model = Iniziativa

    def get_context_data(self, **kwargs):
        kwargs.update({'object_name': 'Iniziative'})
        return kwargs


class SubIniziativaMixin(object):
    model = SottoIniziativa

    def get_context_data(self, **kwargs):
        kwargs.update({'object_name': 'Sotto Iniziative'})
        return kwargs


class GruppoMixin(object):
    model = Raggruppamento

    def get_context_data(self, **kwargs):
        kwargs.update({'object_name': 'Raggruppamento'})
        return kwargs


class SottoIniziativaForm(ModelForm):
    """
    Attenzione che il campo iniziativa che è una chiave esterna non lo metto proprio così il form potrà essere
    validato senza errori.
    Dopo la validazione scrivo la chiave esterna e poi lo salvo ma tutto questo lo farò nella view !
    """
    class Meta:
        model = SottoIniziativa
        fields = ['nome', 'descrizione', 'in_uso']


class GruppoForm(ModelForm):
    """
    Attenzione che il campo sotto-iniziativa che è una chiave esterna non lo metto proprio così il form potrà essere
    validato senza errori.
    Dopo la validazione scrivo la chiave esterna e poi lo salvo ma tutto questo lo farò nella view !
    """
    class Meta:
        model = Raggruppamento
        fields = ['nome', 'descrizione', 'ordine', 'in_uso']