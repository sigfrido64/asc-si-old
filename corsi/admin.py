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
    fields = ('codice', 'denominazione', 'durata', 'data_inizio', 'data_fine', 'data_aggiornamento',
              'iniziativa', 'sotto_iniziativa', 'raggruppamento')
    readonly_fields = ('data_aggiornamento',)


admin.site.register(Corso, CorsoAdmin)          # Registro l'interfaccia amministrativa per i corsi


