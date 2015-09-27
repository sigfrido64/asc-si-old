# coding=utf-8
"""
    Corsi
"""
from django.db import models

"""
    Costanti per i valori di default
"""
DEFAULT_PROVINCIA = 'TO'
DEFAULT_NAZIONE_ID = 181


class Nazioni(models.Model):
    """
    Definizione degli Stati da Elenco a Discesa
    """
    nazione = models.CharField(max_length=100, unique=True)
    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nazione

    class Meta:
        verbose_name = "Nazione"
        verbose_name_plural = "Nazioni"


class Provincie(models.Model):
    """
    Definizione delle Provincie, solo per l'ITALIA
    """
    provincia = models.CharField(max_length=100, unique=True)
    sigla = models.CharField(max_length=2, primary_key=True)
    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.provincia + "(" + self.sigla + ")"

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincie"


class Categoria(models.Model):
    """
    Definizione delle Categorie
    """
    categoria = models.CharField(max_length=80, unique=True)
    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categoria

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorie"


class Azienda(models.Model):
    """
    Definizione dell'Anagrafica di un' Azienda
    """
    ragione_sociale = models.CharField(max_length=100)
    descrizione = models.CharField(max_length=200, blank=True)
    indirizzo1 = models.CharField(max_length=50)
    indirizzo2 = models.CharField(max_length=50, blank=True)
    comune = models.CharField(max_length=50)
    provincia = models.ForeignKey(Provincie, default=DEFAULT_PROVINCIA)
    nazione = models.ForeignKey(Nazioni, default=DEFAULT_NAZIONE_ID)
    cap = models.CharField(max_length=10, blank=True)
    piva = models.CharField(max_length=14, blank=True)
    cf = models.CharField(max_length=16, blank=True)
    tel1 = models.CharField(max_length=30, blank=True)
    tel2 = models.CharField(max_length=30, blank=True)
    tel3 = models.CharField(max_length=30, blank=True)
    tel4 = models.CharField(max_length=30, blank=True)
    doctel1 = models.CharField(max_length=20, blank=True)
    doctel2 = models.CharField(max_length=20, blank=True)
    doctel3 = models.CharField(max_length=20, blank=True)
    doctel4 = models.CharField(max_length=20, blank=True)
    sito_web = models.CharField(max_length=50, blank=True)
    sede_legale = models.BooleanField(default=False)
    attivo = models.BooleanField(default=True)
    promozione_ok = models.BooleanField(default=True)
    note = models.TextField(blank=True)
    categorie = models.ManyToManyField(Categoria)
    hash = models.CharField(max_length=100)
    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ragione_sociale

    class Meta:
        verbose_name = "Azienda"
        verbose_name_plural = "Aziende"


class Contatto(models.Model):
    """
    Definizione di un contatto aziendale
    """
    azienda = models.ForeignKey(Azienda)
    titolo = models.CharField(max_length=20, blank=True, default='')
    nome = models.CharField(max_length=50, blank=True, default='')
    secondo_nome = models.CharField(max_length=50, blank=True, default='')
    cognome = models.CharField(max_length=50)
    posizione = models.CharField(max_length=50, blank=True, default='')
    tel1 = models.CharField(max_length=30, blank=True, default='')
    tel2 = models.CharField(max_length=30, blank=True, default='')
    tel3 = models.CharField(max_length=30, blank=True, default='')
    tel4 = models.CharField(max_length=30, blank=True, default='')
    doctel1 = models.CharField(max_length=20, blank=True, default='')
    doctel2 = models.CharField(max_length=20, blank=True, default='')
    doctel3 = models.CharField(max_length=20, blank=True, default='')
    doctel4 = models.CharField(max_length=20, blank=True, default='')
    email1 = models.EmailField(blank=True, default='')
    email2 = models.EmailField(blank=True, default='')
    data_nascita = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, default='')
    categorie = models.ManyToManyField(Categoria)
    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)
