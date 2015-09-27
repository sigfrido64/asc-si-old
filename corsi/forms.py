# coding=utf-8
from django.forms import Textarea, TextInput
from .models import Corso
from mongodbforms import DocumentForm


class CorsoForm(DocumentForm):
    class Meta:
        model = Corso
        fields = ['codice_edizione', 'denominazione', 'durata', 'ordine', 'note']

        widgets = {
            'codice_edizione': TextInput(attrs={'class': 'easyui-textbox'}),
            'denominazione': TextInput(attrs={'class': 'easyui-textbox', 'style': 'width:300px'}),
            'durata': TextInput(attrs={'class': 'easyui-textbox'}),
            'ordine': TextInput(attrs={'class': 'easyui-textbox'}),
            'note': Textarea(attrs={'class': 'easyui-textbox', 'data-options': 'multiline:true',
                                    'style': 'width:300px;height:100px'}),
        }
