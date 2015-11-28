# coding=utf-8
from django.http import Http404
from mongoengine import fields, Document
from tasker.models import Heartbeats
import datetime


class UserPermissions(Document):
    user = fields.StringField(primary_key=True)
    permissions = fields.ListField(fields.StringField(max_length=10))


def get_obj_or_404(klass, *args, **kwargs):
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        raise Http404


def heartbeat(processo, timeout):
    """
    Gestisce

    :param processo: Nome del processo che sto monitorando
    :param timeout: Timeout in secondi trascorso il quale si deve pensare che il processo sia abortito
    :return: Nulla. Tutti i dati vengono salvati nel data base di appoggio.
    """
    hb = Heartbeats()
    hb.processo = processo
    hb.timeout = timeout
    hb.data_aggiornamento = datetime.datetime.now()
    hb.save()


def stampadebug(messaggio, debug_flag):
        """
        Stampa un messaggio di debug.

        :param messaggio: il messaggio da stampare se DEBUG_PRINT è True, altrimenti non fa nulla.
        :param debug_flag: flag che dice se devo o meno stampare il messaggio. In questo modo posso abilitare la
                           stampa di debug per il singolo modulo.
        :return: None
        """
        if debug_flag:
            print(messaggio)
