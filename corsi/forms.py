# coding=utf-8
from django.forms import Textarea, TextInput, Select
from .models import Corso
from mongodbforms import DocumentForm


def automastati(stato):
    if stato == 0:
        return """
            valueField: 'value',
            textField: 'label',
            data: [{
                label: 'Bozza',
                value: '0'
            },{
                label: 'Pianificato',
                value: '10'
            }]
        """


class CorsoForm(DocumentForm):
    class Meta:
        model = Corso
        fields = ['codice_edizione', 'denominazione', 'ordine', 'durata', 'partecipanti', 'docente',
                  'note', 'stato']

        widgets = {
            'codice_edizione': TextInput(attrs={'class': 'easyui-textbox'}),
            'denominazione': TextInput(attrs={'class': 'easyui-textbox', 'style': 'width:300px'}),
            'durata': TextInput(attrs={'class': 'easyui-textbox'}),
            'ordine': Select(attrs={'class': 'easyui-combobox'}),
            'partecipanti': TextInput(attrs={'class': 'easyui-textbox'}),
            'docente': TextInput(attrs={'class': 'easyui-textbox'}),
            'note': Textarea(attrs={'class': 'easyui-textbox', 'data-options': 'multiline:true',
                                    'style': 'width:300px;height:100px'}),
            'stato': TextInput(attrs={'class': 'easyui-combobox', 'data-options': automastati(0)})
        }
