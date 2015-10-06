# coding=utf-8
from django.forms import Textarea, TextInput, Select
from .models import Corso
from mongodbforms import DocumentForm


class CorsoForm(DocumentForm):
    class Meta:
        model = Corso
        fields = ['codice_edizione', 'denominazione', 'ordine', 'durata', 'note']

        widgets = {
            'codice_edizione': TextInput(attrs={'class': 'easyui-textbox'}),
            'denominazione': TextInput(attrs={'class': 'easyui-textbox', 'style': 'width:300px'}),
            'durata': TextInput(attrs={'class': 'easyui-textbox'}),
            'ordine': Select(attrs={'class': 'easyui-combobox'}),
            'note': Textarea(attrs={'class': 'easyui-textbox', 'data-options': 'multiline:true',
                                    'style': 'width:300px;height:100px'}),
        }
