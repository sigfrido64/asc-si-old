# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import CorsoForm
from .models import Corso, UserPermissions
from django.core.urlresolvers import reverse
import json


def get_obj_or_404(klass, *args, **kwargs):
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        raise Http404


@login_required()
def index(request):
    """
    Lista dei corsi in ordine alfabetico
    """
    perm = get_obj_or_404(UserPermissions, user=request.user.get_username())
    if 'corsi' not in perm.permissions:
        return Http404

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
        print(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
           #  post['data_inizio'] = form.cleaned_data['data1']
            post.save()
            return HttpResponseRedirect(reverse('corsi:index'))
        else:
            print(form.errors)

    else:
        form = CorsoForm(instance=corso, initial={'data1': '10/09/2014'})

    # Popola il dizionario per il template.
    context_dict = {'form': form}

    # Visualizza il template.
    return render(request, 'corsi/add_edit.html', context_dict)

"""
@login_required()
def corso_add(request):
    CORSO : Aggiunta di un nuovo corso.

    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = CorsoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return HttpResponseRedirect(reverse('iniziative:detail', kwargs={'pk_iniziativa': pk_iniziativa}))
        else:
            print(form.errors)
    else:
        form = CorsoForm()

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'iniziativa': iniziativa}

    # Visualizza il template.
    return render(request, 'iniziative/sub_cu.html', context_dict)
"""

#
# Sezione API
#
def get_corsi(request):
    print("Chiamata")
    if request.is_ajax():
        # q = request.GET.get('term', '')
        corsi = Corso.objects.all()
        results = []
        for corso in corsi:
            corsi_json = {}
            corsi_json['id'] = corso.pk
            corsi_json['codice'] = corso.codice_edizione
            corsi_json['denominazione'] = corso.denominazione
            results.append(corsi_json)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
