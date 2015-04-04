# coding=utf-8
"""
    Interfaccia amministrativa per i corsi
"""
from django.contrib import admin
from .models import Corso


class CorsoAdmin(admin.ModelAdmin):
    """
    Sistemo l'interfaccia di default per mostrare i campi dei corsi
    """
    fields = ('codice_edizione', 'denominazione', 'durata', 'data_inizio', 'data_fine', 'stato', 'raggruppamento',
              'note',)

admin.site.register(Corso, CorsoAdmin)          # Registro l'interfaccia amministrativa per i corsi

