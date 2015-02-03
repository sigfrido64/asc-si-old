# coding=utf-8
"""
    Corsi
"""

from django.db import models
from django.core.validators import MinLengthValidator, ValidationError



class Corso(models.Model):
    """
    Definizione dei corsi
    """
    codice = models.CharField(primary_key=True, max_length=10, validators=[MinLengthValidator(6)])
    denominazione = models.CharField(max_length=100, validators=[MinLengthValidator(5)])
    data_inizio = models.DateField()
    data_fine = models.DateField()
    raggruppamento = models.ForeignKey('iniziative.Raggruppamento')
    durata = models.IntegerField(default=8)
    data_aggiornamento = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Corso"
        verbose_name_plural = "Corsi"

    def __str__(self):
        return self.codice

    def clean(self):
        """
            Validazione del modello nel suo complesso.
            Così non si lega al campo ! Non va bene !
        """
        # La durata del corso deve essere di alemo un'ora.
        if self.durata <= 0:
            raise ValidationError({'durata': 'La durata del corso deve essere positiva.'})

        # La data di inizio deve essere maggiore o uguale a quella di fine.
        if self.data_fine < self.data_inizio:
            raise ValidationError({'data_fine': 'La data di fine corso deve essere maggiore o uguale a quella '
                                                'di inizio corso.'})


"""
    TODO
        Regole di verifica per validare il corso ed ambiente di test per le prove.
        Codice corso con le sue regole e tutto maiuscolo !
"""