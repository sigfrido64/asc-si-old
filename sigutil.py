# coding=utf-8
from django.http import Http404
from mongoengine import fields, Document


class UserPermissions(Document):
    user = fields.StringField(primary_key=True)
    permissions = fields.ListField(fields.StringField(max_length=10))


def get_obj_or_404(klass, *args, **kwargs):
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        raise Http404
