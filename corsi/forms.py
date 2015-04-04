# coding=utf-8
__author__ = 'Sig'


from django import forms
from .models import Corso


class CorsoForm(forms.ModelForm):

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Corso
        fields = ('codice_edizione', 'denominazione', 'data_inizio', 'data_fine', 'durata', 'stato', 'raggruppamento',
                  'note')