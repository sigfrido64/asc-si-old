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
    BOZZA = 0
    PIANIFICATO = 10

    STATO_CORSO_CHOICES = (
        (BOZZA, u'Bozza'),
        (PIANIFICATO, u'Pianificato'),
    )

    codice_edizione = models.CharField(primary_key=True, max_length=10, validators=[MinLengthValidator(6)])
    denominazione = models.CharField(max_length=150, validators=[MinLengthValidator(10)])
    data_inizio = models.DateField()
    data_fine = models.DateField()
    durata = models.IntegerField(default=8)
    stato = models.IntegerField(choices=STATO_CORSO_CHOICES, default=BOZZA)
    raggruppamento = models.ForeignKey('iniziative.Raggruppamento')
    # modello = models.ForeignKey(Modello)
    note = models.CharField(max_length=1000)

    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Corso"
        verbose_name_plural = "Corsi"

    def __str__(self):
        return self.codice_edizione + ' ' + self.denominazione

    def clean(self):
        """
            Validazione del modello nel suo complesso.
        """
        # La durata del corso deve essere di almeno un'ora.
        if self.durata <= 0:
            raise ValidationError({'durata': 'La durata del corso deve essere positiva.'})

        # La data di inizio deve essere maggiore o uguale a quella di fine.
        if self.data_fine < self.data_inizio:
            raise ValidationError({'data_fine': 'La data di fine corso deve essere maggiore o uguale a quella '
                                                'di inizio corso.'})
        self.codice_edizione = self.codice_edizione.upper()
