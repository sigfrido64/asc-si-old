from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Azienda
import json


# region API per i form JSON
@login_required()
def get_listaziende(request):
    print("Chiamata AJAX Aziende")
    if request.is_ajax():
        ini = request.GET.get('q', '')
        print('iniziali = ', ini)
        if len(ini) < 3:
            return
        try:
            # Recupera le prime 20 aziende con le iniziali date.
            # Sarà da migliorare con la ricerca full text di Mongo ? TODO
            aziende = Azienda.objects.filter(ragione_sociale__icontains=ini)
        except Azienda.DoesNotExist:
            # Se non trova aziende con quel testo pazienza, vuol dire che non ce ne sono
            pass
        results = []
        for azienda in aziende:
            stringa_json = {}
            stringa_json['name'] = azienda.ragione_sociale + ' - ' + azienda.indirizzo1 + ' - ' + azienda.comune
            stringa_json['id'] = azienda.pk
            results.append(stringa_json)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
# endregion
