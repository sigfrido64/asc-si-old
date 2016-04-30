# coding=utf-8
from django.shortcuts import render
from .models import Nazione, NazioneSQL
from .models import Azienda, Sede, Contatto
from .models import Provincia, ProvinciaSQL, AziendaSQL, ContattoSQL
from .models import AziendaHelper, SedeHelper, ContattoHelper
from .forms import AziendaForm
from sigutil import UserPermissions, get_obj_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from bson.json_util import dumps
from sigutil import concatena, valid_email, hashsig


# region API Helpers
def aggiornahelper(azienda_id):
    """
    Aggiorna il record correlato nella collection di helper.
    :param azienda_id: Id dell'azienda di cui ricreo l'helper entry.
    """
    # DEBUG print("Id : " + str(azienda_id))
    # Come prima cosa recupera il record se esiste oppure ne crea uno nuovo.
    try:
        aziendah = AziendaHelper.objects.get(id=azienda_id)
    except AziendaHelper.DoesNotExist:
        aziendah = AziendaHelper()
    # Recupera il record dell'azienda per le future referenze. Lo faccio perchè MongoDB non supporta i Join.
    azienda = Azienda.objects.get(id=azienda_id)
    # Copia gli elementi relativi all'azienda.
    aziendah.ragione_sociale = azienda.ragione_sociale
    aziendah.id = azienda.id
    aziendah.descrizione = azienda.descrizione
    aziendah.id_asc_azienda = azienda.id_asc_azienda

    # Ripulisce il record delle sede se esiste.
    del aziendah.sedi[:]

    # Ora recupera ogni sede.
    sedi = Sede.objects(azienda=azienda)
    for sede in sedi:
        # Copia gli elementi relativi alla sede.
        sh = SedeHelper()
        sh.id = sede.id
        sh.indirizzo = concatena(sede.indirizzo1, " ", sede.indirizzo2, " - ", sede.cap, " ", sede.comune, " (",
                                 sede.provincia, ")")
        if sede.nazione:
            sh.indirizzo = concatena(sh.indirizzo, " - ", sede.nazione)

        # E per ogni sede recupera ogni contatto.
        contatti = Contatto.objects(azienda=azienda)
        for conta in contatti:
            ch = ContattoHelper()
            ch.contatto = concatena(conta.titolo, " ", conta.cognome, " ", conta.nome)
            ch.id = conta.pk
            ch.id_asc_contatto = conta.id_asc_contatto
            sh.contatti.append(ch)

        aziendah.sedi.append(sh)

    # Salva il tutto.
    return aziendah.save()


@csrf_exempt
def api_refreshelper(request):
    print("Refresh helper aziende")
    cavolo = Azienda.objects()
    for azienda in cavolo:
        # DEBUG print(azienda.ragione_sociale)
        aggiornahelper(azienda.pk)

    mimetype = 'application/json'
    return HttpResponse("Aggiornamento Terminato !", mimetype)
# endregion


@login_required()
def index(request):
    """
    Pagina iniziale delle aziende.
    :param request:
    """
    # Recupera le permission dell'utente e verifica che sia abilitato a visualizzare questa pagina.
    perm = get_obj_or_404(UserPermissions, user=request.user.get_username())
    if UserPermissions.AZIENDE_ALL not in perm.permissions:
        return Http404

    # Popola il context dict e visualizza la pagina.
    context_dict = {'perm': perm}
    return render(request, 'aziende/index.html', context_dict)


@login_required()
def add_edit(request, pk=None):
    """
    Aggiunge o edita un' Azienda.
    :param request: Handle della richiesta.
    :param pk: id dell'azienda se la sto editando.
    :return: None
    """
    # TODO qui ci vuole una permission specifica per le aziende.
    perm = get_obj_or_404(UserPermissions, user=request.user.get_username())
    if 'aziende' not in perm.permissions:
        return Http404

    # Se è specificata una pk prova a recuperare il record altrimenti si tratta di un inserimento e procedo oltre.
    if pk:
        azienda = get_obj_or_404(Azienda, id=pk)
    else:
        azienda = Azienda()

    if request.method == 'POST':
        form = AziendaForm(request.POST, instance=azienda)
        if form.is_valid():
            form.save
            return HttpResponseRedirect(reverse('aziende:index'))
    else:
        form = AziendaForm(instance=azienda)
    # Popola il dizionario per il template.
    context_dict = {'form': form, 'perm': perm}
    # Visualizza il template.
    return render(request, 'aziende/az_add_edit.html', context_dict)


# region API Aziende
@csrf_exempt
def get_listanazioni(request):
    print("Chiamata AJAX Aziende")
    if request.is_ajax() or True:
        results = []
        for nazione in Nazione.objects():
            stringa_json = {}
            stringa_json['OrderID'] = 1
            stringa_json['CustomerID'] = nazione.nazione
            stringa_json['EmployeeID'] = 'Sigfrido'
            results.append(stringa_json)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@csrf_exempt
def get_listaziende(request):
    filtro = hashsig(request.GET.get('filtroAzienda', '')).upper()
    print("Filtro = " + filtro)
    if request.is_ajax() or True:
        results = []

        aziende = AziendaHelper.objects(hash_azienda__contains=filtro).explain()
        print(aziende)
        aziende = AziendaHelper.objects(hash_azienda__contains=filtro)[:50]
        for azienda in aziende:
            stringa_json = {}
            stringa_json['pk'] = str(azienda.pk)
            stringa_json['ragione_sociale'] = azienda.ragione_sociale
            stringa_json['sedi'] = azienda.sedi_html
            stringa_json['contatti'] = azienda.contatti_html
            results.append(stringa_json)


        data = dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@csrf_exempt
def popola(request):
    azienda1 = Azienda()
    azienda1.ragione_sociale = "Ciccio e Pluto"
    azienda1.cf = "1234"
    azienda1.note = "Nessuna"

    sede1 = Sede()
    sede1.indirizzo1 = "via posalaquaglia 1"
    sede1.cap = "10100"
    sede1.comune = "torino"

    azienda1.sedi.append(sede1)

    sede2 = Sede()
    sede2.indirizzo1 = "via merdacane 1"
    sede2.cap = "10101"
    sede2.comune = "Cinisello"

    azienda1.sedi.append(sede2)

    azienda1.save()  # Prima azienda

    azienda = Azienda()
    azienda.ragione_sociale = "Pluto e Paperino"
    azienda.cf = "12345"
    azienda.note = "Nessuna"

    sede1 = Sede()
    sede1.indirizzo1 = "via della polverirei 1"
    sede1.cap = "10100"
    sede1.comune = "torino"

    azienda.sedi.append(sede1)

    sede2 = Sede()
    sede2.indirizzo1 = "via cazzo e culo 1"
    sede2.cap = "10101"
    sede2.comune = "Cinisello"

    azienda.sedi.append(sede2)

    azienda.save()  # Seconda Azienda.

    return HttpResponseRedirect(reverse('aziende:index'))
# endregion


# region API IMPORTAZIONE ASSOCAM
def importanazioni(request):
    """
    Importa la lista delle nazioni partendo da un database SQlite3 con il modello impostato in models
    nel database mongo !

    TODO Considerare gli iteratori con grossi recordset !
    star_set = Star.objects.all()
    # The `iterator()` method ensures only a few rows are fetched from
    # the database at a time, saving memory.
    for star in star_set.iterator():
        print(star.name)
    """
    for nazione_sql in NazioneSQL.objects.all():
        nazione = Nazione()
        nazione.nazione = nazione_sql.nazione
        nazione.save()

    # Visualizza la risposta.
    return HttpResponse("Nazioni Importate con successo")


def importaprovincie(request):
    """
    Importa la lista delle provincie partendo da un database SQlite3 con il modello impostato in models
    nel database mongo !
    """
    for provincia_sql in ProvinciaSQL.objects.all():
        provincia = Provincia()
        provincia.sigla = provincia_sql.sigla
        provincia.provincia = provincia_sql.provincia
        provincia.save()

    # Visualizza la risposta.
    return HttpResponse("Provincie Importate con successo")


def importaaziende(request):
    """
    Importa la lista delle aziende e delle sedi delle stesse partendo da un database SQlite3 con il modello
    impostato in models nel database mongo !
    """
    for azienda_sql in AziendaSQL.objects.all():
        print("Importazione azienda : " + str(azienda_sql.id_azienda))
        # Importa i dati dell'azienda.
        azienda = Azienda()
        azienda.id_asc_azienda = azienda_sql.id_azienda
        azienda.ragione_sociale = azienda_sql.ragione_sociale
        azienda.descrizione = azienda_sql.descrizione
        azienda.cf = azienda_sql.cf
        azienda.sito_web = azienda_sql.sitoweb
        azienda.note = azienda_sql.note
        azienda.hash = azienda_sql.hashragionesociale
        # E la salva, così il riferimento ci sarà e sarà valido.
        azienda.save()

        # Adesso inserisce quelli della sede.
        sede = Sede()
        sede.id_asc_azienda = azienda_sql.id_azienda
        sede.indirizzo1 = azienda_sql.indirizzo
        sede.comune = azienda_sql.citta
        sede.provincia = azienda_sql.provincia
        sede.cap = azienda_sql.cap
        sede.piva = azienda_sql.piva
        sede.tel1 = azienda_sql.tel1
        sede.tel2 = azienda_sql.tel2
        sede.tel3 = azienda_sql.tel3
        sede.tel4 = azienda_sql.tel4
        sede.doctel1 = azienda_sql.dtel1
        sede.doctel2 = azienda_sql.dtel2
        sede.doctel3 = azienda_sql.dtel3
        sede.doctel4 = azienda_sql.dtel4
        sede.note = azienda_sql.note
        sede.attivo = (True if azienda_sql.valido else False)
        sede.promozione_ok = (True if azienda_sql.accetta_promozioni else False)

        # Crea il link all'azienda correlata.
        sede.azienda = Azienda.objects.get(id_asc_azienda=azienda_sql.id_azienda)
        # Salva la sede.
        sede.save()

    data = json.dumps("Aziende e Sedi Importate !")
    # Visualizza la risposta.
    return HttpResponse(data)


def importacontatti(request):
    """
    Importa la lista dei contatti delle aziende partendo da un database SQlite3 con il modello impostato in models
    nel database mongo !
    """
    for contatto_sql in ContattoSQL.objects.all():
        print("Importo contatto : " + str(contatto_sql.id_contatto))
        # Importa i dati del contatto.
        contatto = Contatto()
        contatto.id_asc_contatto = contatto_sql.id_contatto
        contatto.id_asc_azienda = contatto_sql.id_azienda
        contatto.titolo = contatto_sql.titolo
        contatto.nome = contatto_sql.nome
        contatto.cognome = contatto_sql.cognome
        contatto.posizione = contatto_sql.posizione
        contatto.tel1 = contatto_sql.tel1
        contatto.tel2 = contatto_sql.tel2
        contatto.tel3 = contatto_sql.tel3
        contatto.tel4 = contatto_sql.tel4
        contatto.doctel1 = contatto_sql.dtel1
        contatto.doctel2 = contatto_sql.dtel2
        contatto.doctel3 = contatto_sql.dtel3
        contatto.doctel4 = contatto_sql.dtel4
        # Se le due email ci sono e sono valide le importa.
        if contatto_sql.email1:
            dummy = contatto_sql.email1.strip()
            if valid_email(dummy):
                contatto.email1 = dummy
        if contatto_sql.email2:
            dummy = contatto_sql.email2.strip()
            if valid_email(dummy):
                contatto.email2 = dummy
        contatto.note = contatto_sql.note

        # Crea il link all'azienda cui si riferisce.
        print("Cerco Azienda con ID : ", contatto_sql.id_azienda)
        # Come prima cosa recupera il record se esiste oppure ne crea uno nuovo.
        try:
            azienda = Azienda.objects.get(id_asc_azienda=contatto_sql.id_azienda)
            contatto.azienda = azienda
            contatto.save()
        except Azienda.DoesNotExist:
            pass

    data = "Contatti Importati"
    # Visualizza la risposta.
    return HttpResponse(data)
# endregion
