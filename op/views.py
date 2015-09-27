# coding=utf-8
# from mongoengine import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import OrdineProduzioneForm
from .models import OrdineProduzione
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse


def get_obj_or_404(klass, *args, **kwargs):
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        raise Http404


@login_required()
def index(request):
    """
    Lista degli ordini di produzione in ordine decrescente di data di inserimento.
    """
    lista_ordini = OrdineProduzione.objects().order_by('ordine_numero')
    context_dict = {'lista_ordini': lista_ordini}

    # Visualizza la risposta.
    return render(request, 'op/index.html', context_dict)


@login_required()
def op_add(request):
    """
    Aggiunge un ordine di produzione.
    OBSOLETO : Al momento lavoro con una sola vista che è quella di EDIT !
    """
    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = OrdineProduzioneForm(request.POST)
        print(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # post['data_inizio'] = form.cleaned_data['data1']
            post.save()
            return HttpResponseRedirect(reverse('op:index'))
        else:
            print(form.errors)
    else:
        form = OrdineProduzioneForm(initial={'data1': '10/09/2014'})

    # Popola il dizionario per il template.
    context_dict = {'form': form}

    # Visualizza il template.
    return render(request, 'op/op_add.html', context_dict)


@login_required()
def op_edit(request, pk=None):
    """
    Aggiunge o edita un ordine di produzione.
    """
    # Se è specificata una pk prova a recuperare il record altrimenti si tratta di un inserimento e procedo oltre.
    if pk:
        ordine = get_obj_or_404(OrdineProduzione, ordine_numero=pk)
    else:
        ordine = OrdineProduzione()

    if request.method == 'POST':
        form = OrdineProduzioneForm(request.POST)
        print(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
           #  post['data_inizio'] = form.cleaned_data['data1']
            post.save()
            return HttpResponseRedirect(reverse('op:index'))
        else:
            print(form.errors)

    else:
        print ("Ordine id : ", ordine.id)
        form = OrdineProduzioneForm(instance=ordine, initial={'data1': '10/09/2014'})
        # print ("Ordine id Form :", form.id)

    # Popola il dizionario per il template.
    context_dict = {'form': form}

    # Visualizza il template.
    return render(request, 'op/op_add.html', context_dict)
