# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import CorsoForm
from .models import Corso, Lezione, CartelleCorsoTask
from django.core.urlresolvers import reverse
from sigutil import UserPermissions, get_obj_or_404
from bson.objectid import ObjectId
import json


def task_dispatcher(corso, vecchio_stato, nuovo_stato):
    # Passaggio da BOZZA a ...
    if vecchio_stato == 0:
        # PIANIFICATO : Emissione della richiesta di creazione della cartella corso.
        if nuovo_stato == 10:
            newtask = CartelleCorsoTask()
            newtask.corso = corso
            newtask.anno_formativo = "2015-2016"  # TODO Questo deve arrivare dal corso
            newtask.tipologia = "FAP"    # TODO Questo deve arrivare dal corso
            newtask.save()
    return


@login_required()
def index(request):
    """
    Lista dei corsi in ordine alfabetico
    """
    # Verifico se l'utente ha il permesso di usare questa vista.
    perm = get_obj_or_404(UserPermissions, user=request.user.get_username())
    if 'corsi' not in perm.permissions:
        return Http404

    # Recupero la lista dei corsi.
    lista_corsi = Corso.objects().order_by('codice_corso')
    context_dict = {'lista_corsi': lista_corsi, 'perm': perm}

    # Visualizza la risposta.
    return render(request, 'corsi/index.html', context_dict)


@login_required()
def add_edit(request, pk=None):
    """
    Aggiunge o edita un corso.
    """
    perm = get_obj_or_404(UserPermissions, user=request.user.get_username())
    if 'corsi' not in perm.permissions:
        return Http404

    # Se è specificata una pk prova a recuperare il record altrimenti si tratta di un inserimento e procedo oltre.
    if pk:
        corso = get_obj_or_404(Corso, codice_edizione=pk)
    else:
        corso = Corso()

    if request.method == 'POST':
        form = CorsoForm(request.POST)
        if form.is_valid():
            # Se si tratta di un aggiornamento valuto eventuali azioni.
            if pk:
                corso_old = get_obj_or_404(Corso, codice_edizione=pk)
                task_dispatcher(corso=corso_old.pk, vecchio_stato=corso_old.stato,
                                nuovo_stato=form.cleaned_data.get('stato'))
            post = form.save(commit=False)
           #  post['data_inizio'] = form.cleaned_data['data1']
            post.save()
            return HttpResponseRedirect(reverse('corsi:index'))
        else:
            print("Macchecazzo")
            print(form.errors)
    else:
        form = CorsoForm(instance=corso, initial={'data1': '10/09/2014'})

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'perm': perm}

    # Visualizza il template.
    return render(request, 'corsi/add_edit.html', context_dict)


# region Corsi Ajax API.
def get_corsi(request):
    """
    :param request: Nessuno specifico.
    :return: Lista completa di tutti i corsi.
    """
    corsi = Corso.objects.all()
    results = []
    for corso in corsi:
        corsi_json = {}
        corsi_json['id'] = corso.pk
        corsi_json['codice'] = corso.codice_edizione
        corsi_json['denominazione'] = corso.denominazione
        results.append(corsi_json)
    data = json.dumps(results)

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
# endregion


# region Lezioni Ajax API.
def lezioni_getall(request):
    """
    Recupera una lista non ordinata delle lezioni associate ad un dato corso.

    :param request: 'corso' : codice di edizione del corso di cui voglio recuperare le lezioni.
    :return: Lista delle lezioni associate al corso.
    """
    # Recupero il corso se esiste.
    corso = request.GET.get('corso', '')
    corso = get_obj_or_404(Corso, codice_edizione=corso)

    # Itero sulle lezioni
    results = []
    for lezione in corso.lezioni:
        lezione_json = {}
        lezione_json['id'] = str(lezione.id)
        lezione_json['data'] = lezione.data
        lezione_json['inizio'] = lezione.inizio
        lezione_json['fine'] = lezione.fine
        lezione_json['ore'] = lezione.ore
        lezione_json['sede'] = lezione.sede

        results.append(lezione_json)

    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def lezione_add(request):
    """
    Aggiunge una lezione ad un dato corso.

    :param request: 'corso' : codice di edizione del corso cui aggiungo una lezione.
    :return: 'success' : 'true' in caso di successo.
    """

    # Recupero il corso se esiste.
    corso = request.GET.get('corso', '')
    corso = get_obj_or_404(Corso, codice_edizione=corso)

    # Creo la nuova lezione.
    lezione = Lezione()
    lezione.id = ObjectId()
    lezione.data = request.GET.get('data', '')
    lezione.inizio = request.GET.get('inizio', '')
    lezione.fine = request.GET.get('fine', '')
    lezione.sede = request.GET.get('sede', '')

    # Appendo al corso.
    corso.lezioni.append(lezione)
    corso.save()

    # Riporta OK.
    results = [{'success': 'true'}]

    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def lezione_upd(request):
    """
    Modifica i dati di una particolare lezione.

    :param request: 'corso' : codice di edizione del corso di cui sto modificando una lezione.
                    'lezID' : id della lezione che sto modificando.
                    'data' : Nuova data della lezione.
                    'inizio' : Nuova ora di inizio della lezione.
                    'fine' : Nuova ora di fine della lezione.
    :return: 'success' : 'true' in caso di successo.
    """
    # Recupero il corso se esiste.
    corso = request.GET.get('corso', '')
    corso = get_obj_or_404(Corso, codice_edizione=corso)
    print("Corso recuperato")

    # Recupero l'id della lezione e la cerco nel DocumentEmbedded del corso.
    lezid = request.GET.get('lezID', '')
    lezione = next((lezione for lezione in corso.lezioni if str(lezione.id) == lezid), None)

    # A questo punto aggiorno i campi con quelli del form.
    lezione.data = request.GET.get('data', '')
    lezione.inizio = request.GET.get('inizio', '')
    lezione.fine = request.GET.get('fine', '')
    lezione.sede = request.GET.get('sede', '')

    # Salvo il tutto.
    corso.save()

    # Riporta OK.
    results = [{'success': 'true'}]

    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def lezione_del(request):
    """
    Elimina la lezione dal corso indicato.

    :param request: 'corso' : codice di edizione del corso da cui sto eliminando una lezione.
                    'lezID' : id della lezione che sto eliminando.
    :return: 'success' : 'true' in caso di successo.
    """
    # Recupero il dati del codice di edizione del corso e della lezione.
    corso = request.GET.get('corso', '')
    lezid = request.GET.get('id', '')

    # Elimino la lezione indicata dal corso in oggetto.
    Corso.objects(codice_edizione=corso).update_one(pull__lezioni__id=Lezione(id=lezid).id)

    # Riporto ok.
    results = [{'success': 'true'}]
    data = json.dumps(results)

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

# endregion
