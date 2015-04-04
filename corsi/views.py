# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .forms import CorsoForm
from .models import Corso


class CorsiListView(ListView):
    model = Corso
    template_name = 'corsi/corsi_index.html'


@login_required()
def corso_add(request):
    """
    CORSO : Aggiunta di un nuovo corso.
    """

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