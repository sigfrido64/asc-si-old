# coding=utf-8
from mongoengine import *
from django.db import models
import datetime
from sigutil import concatena, hashsig
# from bson.objectid import ObjectId
"""
    Attenzione che per far funzionare il tutto bisogna creare un indice sparse su CF per evitare l'inserimento di
    valori duplicati nel codice fiscale (Per questo l'indice deve essere di tipo sparse...).
"""


# region Modello MongoDB
class Nazione(Document):
    """
    Collezione delle nazioni note.
    """
    nazione = StringField(max_length=80, required=True, primary_key=True)

    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()

    def __str__(self):
        return self.nazione

    def save(self, *args, **kwargs):
        if not self.dts_creazione:
            self.dts_creazione = datetime.datetime.now()
        self.dts_aggiornamento = datetime.datetime.now()
        return super(Nazione, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Nazione"
        verbose_name_plural = "Nazioni"
        managed = False


class Provincia(Document):
    """
    Collezione delle Provincie (anche se non esistono più !)
    """
    sigla = StringField(max_length=2, required=True, primary_key=True)
    provincia = StringField(max_length=40)

    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()

    def __str__(self):
        return concatena(self.provincia, " (", self.sigla, ")")

    def save(self, *args, **kwargs):
        if not self.dts_creazione:
            self.dts_creazione = datetime.datetime.now()
        self.dts_aggiornamento = datetime.datetime.now()
        return super(Provincia, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincie"
        managed = False


class Azienda(Document):
    """
    Anagrafica Azienda
    """
    ragione_sociale = StringField(max_length=100, required=True)
    descrizione = StringField(max_length=200)
    # Vecchia chiave primaria di Assocam.
    id_asc_azienda = LongField()
    # TODO Devo essere sicuro che non possano essere inseriti due CF Uguali.
    cf = StringField(max_length=16, verbose_name="Codice Fiscale")
    mail_generica = EmailField()
    sito_web = StringField(max_length=50)
    note = StringField()
    hash = StringField(max_length=100)
    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()
    # Definizione degli indici
    # Nello specifico indice testuale su hash.
    meta = {
        'indexes': ['$hash'],
        'collection': 'aziende_aziende'
    }

    def __str__(self):
        return self.ragione_sociale

    def save(self, *args, **kwargs):
        if not self.dts_creazione:
            self.dts_creazione = datetime.datetime.now()
        self.dts_aggiornamento = datetime.datetime.now()
        return super(Azienda, self).save(*args, **kwargs)

    class Meta:
        managed = False


class Sede(Document):
    """
    Sede di un'Azienda.
    """
    # _id = ObjectIdField(required=True, default=lambda: ObjectId())
    # Riferimento alla vecchia matricola Assocam
    id_asc_azienda = LongField()
    # Riferimento al record correlato dell'Azienda.
    azienda = ReferenceField(Azienda, reverse_delete_rule=DENY)
    # Campi specifici della singola sede.
    piva = StringField(max_length=12)
    indirizzo1 = StringField(max_length=50)
    indirizzo2 = StringField(max_length=50)
    comune = StringField(max_length=50)
    provincia = StringField(max_length=2)
    cap = StringField(max_length=5)
    nazione = StringField(max_length=50)
    indirizzo_verboso = StringField(max_length=100)
    tel1 = StringField(max_length=30)
    tel2 = StringField(max_length=30)
    tel3 = StringField(max_length=30)
    tel4 = StringField(max_length=30)
    doctel1 = StringField(max_length=20)
    doctel2 = StringField(max_length=20)
    doctel3 = StringField(max_length=20)
    doctel4 = StringField(max_length=20)
    sede_legale = BooleanField(default=False)
    attivo = BooleanField(default=True)
    promozione_ok = BooleanField(default=True)
    note = StringField()
    # contatti = EmbeddedDocumentListField(EmbeddedDocumentField(Contatto))
    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()
    # Definizione degli indici.
    # Nello specifico su id_asc_azienda in quanto parte delle ricerche saranno fatte qui.
    meta = {
        'indexes': ['id_asc_azienda'],
        'collection': 'aziende_sedi'
    }

    def __str__(self):
        return self.indirizzo_verboso

    def save(self, *args, **kwargs):
        # Compone l'indirizzo verboso dell'azienda.
        dummy = concatena(self.indirizzo1, " ", self.indirizzo2, " - ", self.cap, " ", self.comune, " (",
                          self.provincia, ")")
        if self.nazione:
            dummy = concatena(dummy, " - ", self.nazione)
        self.indirizzo_verboso = dummy

        if not self.dts_creazione:
            self.dts_creazione = datetime.datetime.now()
        self.dts_aggiornamento = datetime.datetime.now()
        return super(Sede, self).save(*args, **kwargs)

    class Meta:
        managed = False


class Contatto(Document):
    """
    Contatto all'interno di un'azienda.
    """
    # _id = ObjectIdField(required=True, default=lambda: ObjectId())
    # Riferimento alla vecchia matricola Assocam
    id_asc_azienda = LongField()
    id_asc_contatto = LongField()
    # Riferimento al record correlato dell'Azienda.
    azienda = ReferenceField(Azienda, reverse_delete_rule=DENY)
    sede = ReferenceField(Sede, reverse_delete_rule=DENY)
    # Campi specifici della singola sede.
    titolo = StringField(max_length=50)
    nome = StringField(max_length=50)
    cognome = StringField(max_length=50)
    posizione = StringField(max_length=50)
    tel1 = StringField(max_length=30)
    tel2 = StringField(max_length=30)
    tel3 = StringField(max_length=30)
    tel4 = StringField(max_length=30)
    doctel1 = StringField(max_length=20)
    doctel2 = StringField(max_length=20)
    doctel3 = StringField(max_length=20)
    doctel4 = StringField(max_length=20)
    email1 = EmailField()
    email2 = EmailField()
    data_nascita = DateTimeField()
    note = StringField()
    attivo = BooleanField(default=True)
    promozione_ok = BooleanField(default=True)
    # Timestamp di creazione e di aggiornamento.
    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()
    # Definizione degli indici.
    # Nello specifico su id_asc_azienda e su id_asc_contatto in quanto parte delle ricerche saranno fatte qui.
    meta = {
        'indexes': ['id_asc_azienda', 'id_asc_contatto'],
        'collection': 'aziende_contatti'
    }

    def __str__(self):
        return concatena(self.titolo, " ", self.cognome, " ", self.nome)

    def save(self, *args, **kwargs):
        if not self.dts_creazione:
            self.dts_creazione = datetime.datetime.now()
        self.dts_aggiornamento = datetime.datetime.now()
        return super(Contatto, self).save(*args, **kwargs)

    class Meta:
        managed = False


class ContattoHelper(EmbeddedDocument):
    """
    Contatto all'interno di un'azienda.
    """
    id = ObjectIdField(required=True)
    # Riferimento alla vecchia matricola Assocam
    id_asc_contatto = LongField()
    # Campi specifici del documento.
    contatto = StringField(max_length=200)

    class Meta:
        managed = False


class SedeHelper(EmbeddedDocument):
    """
    Sede di un'Azienda per l'helper delle ricerche.
    """
    id = ObjectIdField(required=True)
    # Campi specifici della singola sede.
    indirizzo = StringField(max_length=200)
    contatti = EmbeddedDocumentListField(ContattoHelper)

    class Meta:
        managed = False


class AziendaHelper(Document):
    """
    Helper Class per sveltire le interrogazioni.
    """
    id = ObjectIdField(required=True, primary_key=True)
    ragione_sociale = StringField(max_length=100, required=True)
    descrizione = StringField(max_length=200)
    # Vecchia chiave primaria di Assocam.
    id_asc_azienda = LongField()
    # Lista delle sedi.
    sedi = EmbeddedDocumentListField(SedeHelper)
    sedi_html = StringField(max_length=1000)
    contatti_html = StringField(max_length=1000)
    hash_azienda = StringField(max_length=100, required=True)
    meta = {'collection': 'aziende_helper'}

    def __str__(self):
        return self.ragione_sociale

    def save(self, *args, **kwargs):
        # Salva la lista delle sedi con il <br> in html.
        lista_sedi = ''
        for sede in self.sedi:
            if lista_sedi:
                lista_sedi += '<br>'
            lista_sedi += sede.indirizzo
        self.sedi_html = lista_sedi

        # Salva la lista dei contatti in il <br> in html.
        lista_contatti = ''
        for sede in self.sedi:
            for contatto in sede.contatti:
                if lista_contatti:
                    lista_contatti += '<br>'
                lista_contatti += contatto.contatto
        self.contatti_html = lista_contatti

        # Salvo i vari hash per il seguito.
        self.hash_azienda = hashsig(self.ragione_sociale).upper()

        # Chiudo il cerchio con la chiamata al super !
        return super(AziendaHelper, self).save(*args, **kwargs)

    class Meta:
        managed = False

# endregion


# region API IMPORTAZIONE ASSOCAM
class NazioneSQL(models.Model):
    nazione = models.CharField(max_length=80, primary_key=True)

    class Meta:
        managed = False
        db_table = 'asc_nazioni'


class ProvinciaSQL(models.Model):
    sigla = models.CharField(max_length=2, primary_key=True)
    provincia = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'asc_provincie'


class AziendaSQL(models.Model):
    id_azienda = models.IntegerField(primary_key=True, db_column='Id Azienda')
    ragione_sociale = models.CharField(max_length=100, db_column="Ragione Sociale")
    descrizione = models.CharField(max_length=200)
    indirizzo = models.CharField(max_length=50)
    citta = models.CharField(max_length=50)
    provincia = models.CharField(max_length=2)
    cap = models.CharField(max_length=5)
    piva = models.CharField(max_length=12)
    cf = models.CharField(max_length=16)
    tel1 = models.CharField(max_length=30)
    tel2 = models.CharField(max_length=30)
    tel3 = models.CharField(max_length=30)
    tel4 = models.CharField(max_length=30)
    dtel1 = models.CharField(max_length=20)
    dtel2 = models.CharField(max_length=20)
    dtel3 = models.CharField(max_length=20)
    dtel4 = models.CharField(max_length=20)
    sitoweb = models.CharField(max_length=50)
    note = models.CharField(max_length=5000)
    hashragionesociale = models.CharField(max_length=100)
    valido = models.BooleanField()
    accetta_promozioni = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'asc_aziende'


class ContattoSQL (models.Model):
    id_contatto = models.IntegerField(primary_key=True, db_column='Id Contatto')
    id_azienda = models.IntegerField(db_column='Id Azienda')
    titolo = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    posizione = models.CharField(max_length=50)
    tel1 = models.CharField(max_length=30)
    tel2 = models.CharField(max_length=30)
    tel3 = models.CharField(max_length=30)
    tel4 = models.CharField(max_length=30)
    dtel1 = models.CharField(max_length=20)
    dtel2 = models.CharField(max_length=20)
    dtel3 = models.CharField(max_length=20)
    dtel4 = models.CharField(max_length=20)
    email1 = models.CharField(max_length=20)
    email2 = models.CharField(max_length=20)
    data_nascita = models.DateField(db_column='Data Nascita')
    note = models.CharField(max_length=5000)

    class Meta:
        managed = False
        db_table = 'asc_contatti'


# endregion
"""
CREATE TABLE [dbo].[Tabella Membri Aziende](
	[Id Contatto] [int] IDENTITY(1,1) NOT NULL,
	[Id Azienda] [int] NOT NULL,
	[Titolo] [nvarchar](50) NOT NULL,
	[Nome] [nvarchar](50) NOT NULL,
	[Cognome] [nvarchar](50) NOT NULL,
	[Posizione] [nvarchar](50) NOT NULL,
	[Tel1] [nvarchar](30) NULL,
	[Tel2] [nvarchar](30) NULL,
	[Tel3] [nvarchar](30) NULL,
	[Tel4] [nvarchar](30) NULL,
	[DTel1] [nvarchar](20) NULL,
	[DTel2] [nvarchar](20) NULL,
	[DTel3] [nvarchar](20) NULL,
	[DTel4] [nvarchar](20) NULL,
	[Email1] [nvarchar](50) NULL,
	[Email2] [nvarchar](50) NULL,
	[Data Nascita] [datetime] NULL,
	[Note] [ntext] NULL,
	[Flag Saldatura] [bit] NOT NULL,
	[Flag Informatica] [bit] NOT NULL,
	[Flag Sicurezza] [bit] NOT NULL,
	[Flag Qualità] [bit] NOT NULL,
	[Flag Meccanica] [bit] NOT NULL,
	[Flag Automazione] [bit] NOT NULL,
	[Flag Plasturgia] [bit] NOT NULL,
	[Flag Altro] [bit] NOT NULL,
	[TsAggiornamento] [datetime] NULL,
 CONSTRAINT [PK_Tabella Membri Aziende] PRIMARY KEY CLUSTERED

 CREATE TABLE [dbo].[Anagrafica Aziende](
	[Id Azienda] [int] IDENTITY(1,1) NOT NULL,
	[Ragione Sociale] [nvarchar](100) NOT NULL,
	[Descrizione] [nvarchar](200) NULL,
	[Indirizzo] [nvarchar](50) NOT NULL,
	[Città] [nvarchar](50) NOT NULL,
	[Provincia] [nvarchar](2) NULL,
	[CAP] [nvarchar](5) NULL,
	[PIVA] [nvarchar](12) NULL,
	[CF] [nvarchar](16) NULL,
	[Tel1] [nvarchar](30) NULL,
	[Tel2] [nvarchar](30) NULL,
	[Tel3] [nvarchar](30) NULL,
	[Tel4] [nvarchar](30) NULL,
	[DTel1] [nvarchar](20) NULL,
	[DTel2] [nvarchar](20) NULL,
	[DTel3] [nvarchar](20) NULL,
	[DTel4] [nvarchar](20) NULL,
	[SitoWeb] [nvarchar](50) NULL,
	[Note] [ntext] NULL,
	[Flag Saldatura] [bit] NOT NULL,
	[Flag Informatica] [bit] NOT NULL,
	[Flag Sicurezza] [bit] NOT NULL,
	[Flag Qualità] [bit] NOT NULL,
	[Flag Meccanica] [bit] NOT NULL,
	[Flag Automazione] [bit] NOT NULL,
	[Flag Plasturgia] [bit] NOT NULL,
	[Flag Altro] [bit] NOT NULL,
	[HashRagioneSociale] [nvarchar](100) NULL,
	[Valido] [bit] NOT NULL,
	[Accetta_Promozioni] [bit] NOT NULL,
	[Fornitore] [bit] NOT NULL,
	[Mail-Azienda] [nvarchar](80) NULL,
	[TsAggiornamento] [datetime] NULL,
 CONSTRAINT [PK_Anagrafica Aziende] PRIMARY KEY CLUSTERED
"""
