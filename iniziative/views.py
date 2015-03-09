# coding=utf-8
"""
 Ulcuni siti interessanti quanto a gestione del Fors.
 http://www.onespacemedia.com/news/2014/feb/5/getting-started-generic-class-based-views-django/
 http://tumivn.com/2014/09/16/develop-a-crud-movie-app-with-django-1-7/

 ORDINE GENEALE DELLE VISTE

 Index
 Add
 Edit
 Delete
 Detail
"""
# from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.urlresolvers import reverse
from .models import Iniziativa, SottoIniziativa, Raggruppamento
from .forms import SottoIniziativaForm, GruppoForm, GruppoMixin
from django.views.generic import CreateView, UpdateView, DeleteView


# region INIZIATIVE
@login_required()
def index(request):
    """
    INIZIATIVA : Indice generale ordinato per chiave primaria.
    """
    lista_iniziative = Iniziativa.objects.filter(in_uso=True).order_by('pk')
    context_dict = {'lista_iniziative': lista_iniziative}

    # Visualizza la risposta.
    return render(request, 'iniziative/i_index.html', context_dict)


class IniziativaAdd(CreateView):
    """
    INIZIATIVA : Creazione di una nuova iniziativa. !! Login required gestito in urls !!
    """
    model = Iniziativa
    template_name = 'iniziative/i_cu.html'
    success_url = '/si/iniziative/'


class IniziativaEdit(UpdateView):
    """
    INIZIATIVA : Modifica dei dati di un'iniziativa. !! Login required gestito in urls !!
    """
    template_name = 'iniziative/i_cu.html'
    model = Iniziativa
    success_url = '/si/iniziative/'


@login_required()
def iniziativa_delete(request, pk):
    """
    INIZIATIVA : Elimina l'iniziativa data se non ha figli.
    """
    # Cerca di recuperare l'iniziativa e se non ci riesce segnala errore.
    try:
        iniziativa = Iniziativa.objects.get(pk=pk)
    except Iniziativa.DoesNotExist:
        raise Http404("Indice iniziativa inesistente !")

    if iniziativa.sottoiniziativa_set.count() > 0:
        context_dict = {'elemento': iniziativa,
                        'correlati': iniziativa.sottoiniziativa_set.all(),
                        'indietro': reverse('iniziative:index')}
        return render(request, 'e_delcorr.html', context_dict)

    # Se è un POST vuol dire che ci sono già passato e che ho confermato la cancellazione, quindi eseguo.
    if request.method == 'POST':
        iniziativa.delete()
        return HttpResponseRedirect(reverse('iniziative:index'))
    else:
        # Altrimenti visualizzo il form con la domanda se voglio cancellare.
        context_dict = {'iniziativa': iniziativa}
        return render(request, 'iniziative/i_del.html', context_dict)


@login_required()
def detail(request, pk_iniziativa):
    """
    INIZIATIVA : Visualizzazione dei dettagli di un'iniziativa.
    """
    context_dict = {}

    try:
        # Recupero l'iniziativa da visualizzare.
        iniziativa = Iniziativa.objects.get(pk=pk_iniziativa)
        context_dict['iniziativa'] = iniziativa

        # Recupero tutte le sottoiniziative correlate.
        sottoiniziative = SottoIniziativa.objects.filter(iniziativa=pk_iniziativa)
        context_dict['sottoiniziative'] = sottoiniziative

    except Iniziativa.DoesNotExist:
        # Se l'Iniziativa non esiste arrivo qui in modo silente e con il dizionario vuoto per cui il template
        # visualizzerà : Nessuna iniziativa presente.
        pass

    # Visualizza il template.
    return render(request, 'iniziative/i_dtl.html', context_dict)
# endregion


# region SOTTO-INIZIATIVE
@login_required()
def sottoiniziativa_add(request, pk_iniziativa):
    """
    SOTTO-INIZIATIVA : Data un'iniziativa ci aggiunge una sotto iniziativa.
    """
    # Cerca di recuperare l'iniziativa e se non ci riesce segnala errore.
    try:
        iniziativa = Iniziativa.objects.get(pk=pk_iniziativa)
    except Iniziativa.DoesNotExist:
        raise Http404("Indice iniziativa inesistente !")

    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = SottoIniziativaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.iniziativa = iniziativa
            post.save()
            return HttpResponseRedirect(reverse('iniziative:detail', kwargs={'pk_iniziativa': pk_iniziativa}))
        else:
            print(form.errors)
    else:
        form = SottoIniziativaForm()

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'iniziativa': iniziativa}

    # Visualizza il template.
    return render(request, 'iniziative/sub_cu.html', context_dict)


@login_required()
def sottoiniziativa_edit(request, pk):
    """
    SOTTO-INIZIATIVA : Modifica dei dati della sotto iniziativa.
    """
    # Cerca di recuperare la sotto iniziativa e se non ci riesce segnala errore.
    try:
        sottoiniziativa = SottoIniziativa.objects.get(pk=pk)
    except SottoIniziativa.DoesNotExist:
        raise Http404("Indice sotto iniziativa inesistente !")

    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = SottoIniziativaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            sottoiniziativa.nome = post.nome
            sottoiniziativa.descrizione = post.descrizione
            sottoiniziativa.save()
            return HttpResponseRedirect(reverse('iniziative:detail',
                                                kwargs={'pk_iniziativa': sottoiniziativa.iniziativa.pk}))
        else:
            print(form.errors)
    else:
        form = SottoIniziativaForm(instance=sottoiniziativa)

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'iniziativa': sottoiniziativa.iniziativa}

    # Visualizza il template.
    return render(request, 'iniziative/sub_cu.html', context_dict)


@login_required()
def sottoiniziativa_delete(request, pk):
    """
    INIZIATIVA : Elimina l'iniziativa data se non ha figli.
    """
    # Cerca di recuperare l'iniziativa e se non ci riesce segnala errore.
    try:
        sottoiniziativa = SottoIniziativa.objects.get(pk=pk)
    except SottoIniziativa.DoesNotExist:
        raise Http404("Indice iniziativa inesistente !")

    if sottoiniziativa.raggruppamento_set.count() > 0:
        context_dict = {'elemento': sottoiniziativa,
                        'correlati': sottoiniziativa.raggruppamento_set.all(),
                        'indietro': reverse('iniziative:sub_detail', kwargs={'pk_sub': pk})}
        return render(request, 'e_delcorr.html', context_dict)

    # Se è un POST vuol dire che ci sono già passato e che ho confermato la cancellazione, quindi eseguo.
    if request.method == 'POST':
        sottoiniziativa.delete()
        return HttpResponseRedirect(reverse('iniziative:sub_detail', kwargs={'pk_sub': pk}))
    else:
        # Altrimenti visualizzo il form con la domanda se voglio cancellare.
        context_dict = {'sottoiniziativa': sottoiniziativa}
        return render(request, 'iniziative/sub_del.html', context_dict)


@login_required()
def sottoiniziativa_detail(request, pk_sub):
    """
    SOTTO-INIZIATIVA : Visualizzazione dei dettagli della sottoiniziativa.
    """
    context_dict = {}

    try:
        # Recupera la sottoiniziativa.
        sottoiniziativa = SottoIniziativa.objects.get(pk=pk_sub)
        context_dict['sottoiniziativa'] = sottoiniziativa

        # Recupera l'iniziativa padre.
        iniziativa = sottoiniziativa.iniziativa
        context_dict['iniziativa'] = iniziativa

        # Recupera la lista dei raggruppamenti
        raggruppamenti = Raggruppamento.objects.filter(sotto_iniziativa=pk_sub)
        context_dict['raggruppamenti'] = raggruppamenti

    except SottoIniziativa.DoesNotExist:
        # Se la sotto iniziativa non esiste non fa nulla in quanto il caso è già contemplato nel template.
        pass

    # Visualizza il template.
    return render(request, 'iniziative/sub_detail.html', context_dict)
# endregion


# region RAGGRUPPAMENTO
@login_required()
def gruppo_add(request, pk_sub):
    """
    GRUPPO : Data una sotto iniziativa ci aggiunge un gruppo.
    """
    # Cerca di recuperare la sotto iniziativa e se non ci riesce segnala errore.
    try:
        sottoiniziativa = SottoIniziativa.objects.get(pk=pk_sub)
    except SottoIniziativa.DoesNotExist:
        raise Http404("Indice sotto-iniziativa inesistente !")

    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = GruppoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.sotto_iniziativa = sottoiniziativa
            post.save()
            return HttpResponseRedirect(reverse('iniziative:sub_detail', kwargs={'pk_sub': pk_sub}))
        else:
            print(form.errors)
    else:
        form = GruppoForm()

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'sottoiniziativa': sottoiniziativa}

    # Visualizza il template.
    return render(request, 'iniziative/grp_cu.html', context_dict)


@login_required()
def gruppo_edit(request, pk):
    """
    GRUPPO : Modifica dei dati del gruppo.
    """
    # Cerca di recuperare il gruppo e se non ci riesce segnala errore.
    try:
        gruppo = Raggruppamento.objects.get(pk=pk)
    except Raggruppamento.DoesNotExist:
        raise Http404("Indice del raggruppamento inesistente !")

    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = GruppoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            gruppo.nome = post.nome
            gruppo.descrizione = post.descrizione
            gruppo.ordine = post.ordine
            gruppo.save()
            return HttpResponseRedirect(reverse('iniziative:sub_detail',
                                                kwargs={'pk_sub': gruppo.sotto_iniziativa.pk}))
        else:
            print(form.errors)
    else:
        form = GruppoForm(instance=gruppo)

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'sottoiniziativa': gruppo.sotto_iniziativa}

    # Visualizza il template.
    return render(request, 'iniziative/grp_cu.html', context_dict)


class GruppoDelete(GruppoMixin, DeleteView):
    """
    GRUPPO : Cancella il gruppo
    """
    template_name = 'iniziative/grp_del.html'

    def get_success_url(self):
        return reverse('iniziative:sub_detail', kwargs={'pk_sub': self.object.sotto_iniziativa.pk})


@login_required()
def gruppo_detail(request, pk_grp):
    """
    GRUPPO : Visualizzazione dei dettagli del Gruppo.
    """
    context_dict = {}

    try:
        # Recupera il gruppo.
        gruppo = Raggruppamento.objects.get(pk=pk_grp)
        context_dict['gruppo'] = gruppo

        # Recupera la sotto iniziativa padre.
        sottoiniziativa = gruppo.sotto_iniziativa
        context_dict['sottoiniziativa'] = sottoiniziativa

        # Recupera infine l'iniziativa radice
        iniziativa = sottoiniziativa.iniziativa
        context_dict['iniziativa'] = iniziativa

    except Raggruppamento.DoesNotExist:
        # Se il gruppo non esiste non fa nulla in quanto il caso è già contemplato nel template.
        pass

    # Visualizza il template.
    return render(request, 'iniziative/grp_detail.html', context_dict)
# endregion
