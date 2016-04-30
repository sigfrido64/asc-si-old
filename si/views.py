# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sigutil import get_obj_or_404, UserPermissions

__author__ = "Sig"


@login_required
def index(request):
    """
    Visualizzo il form iniziale.
    TODO : Rivedere come cambia con nuovo toolbar !

    :param request: Handle della richiesta
    :return: Mi manda alla pagina iniziale che potrebbe essere diversa a seconda dell'utente.
    """
    # Se l'utente è autenticato vado a cercare i suoi permessi, altrimenti non ne ha nessuno !
    if request.user.is_authenticated():
        perm = get_obj_or_404(UserPermissions, user=request.user.get_username())
    else:
        perm = {}

    # Visualizzo il form iniziale.
    context_dict = {'perm': perm}
    return render(request, 'index.html', context_dict)
