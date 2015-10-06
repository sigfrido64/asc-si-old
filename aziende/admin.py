# coding=utf-8
from django.contrib import admin
from .models import Nazioni, Provincie, Categoria

# Register your models here.
admin.site.register(Nazioni)
admin.site.register(Provincie)
admin.site.register(Categoria)
