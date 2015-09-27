# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Azienda',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('ragione_sociale', models.CharField(max_length=100)),
                ('descrizione', models.CharField(max_length=200, blank=True)),
                ('indirizzo1', models.CharField(max_length=50)),
                ('indirizzo2', models.CharField(max_length=50, blank=True)),
                ('comune', models.CharField(max_length=50)),
                ('cap', models.CharField(max_length=10, blank=True)),
                ('piva', models.CharField(max_length=14, blank=True)),
                ('cf', models.CharField(max_length=16, blank=True)),
                ('tel1', models.CharField(max_length=30, blank=True)),
                ('tel2', models.CharField(max_length=30, blank=True)),
                ('tel3', models.CharField(max_length=30, blank=True)),
                ('tel4', models.CharField(max_length=30, blank=True)),
                ('doctel1', models.CharField(max_length=20, blank=True)),
                ('doctel2', models.CharField(max_length=20, blank=True)),
                ('doctel3', models.CharField(max_length=20, blank=True)),
                ('doctel4', models.CharField(max_length=20, blank=True)),
                ('sito_web', models.CharField(max_length=50, blank=True)),
                ('sede_legale', models.BooleanField(default=False)),
                ('attivo', models.BooleanField(default=True)),
                ('promozione_ok', models.BooleanField(default=True)),
                ('note', models.TextField(blank=True)),
                ('hash', models.CharField(max_length=100)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Aziende',
                'verbose_name': 'Azienda',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('categoria', models.CharField(unique=True, max_length=80)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contatto',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('titolo', models.CharField(default='', blank=True, max_length=20)),
                ('nome', models.CharField(default='', blank=True, max_length=50)),
                ('secondo_nome', models.CharField(default='', blank=True, max_length=50)),
                ('cognome', models.CharField(max_length=50)),
                ('posizione', models.CharField(default='', blank=True, max_length=50)),
                ('tel1', models.CharField(default='', blank=True, max_length=30)),
                ('tel2', models.CharField(default='', blank=True, max_length=30)),
                ('tel3', models.CharField(default='', blank=True, max_length=30)),
                ('tel4', models.CharField(default='', blank=True, max_length=30)),
                ('doctel1', models.CharField(default='', blank=True, max_length=20)),
                ('doctel2', models.CharField(default='', blank=True, max_length=20)),
                ('doctel3', models.CharField(default='', blank=True, max_length=20)),
                ('doctel4', models.CharField(default='', blank=True, max_length=20)),
                ('email1', models.EmailField(default='', blank=True, max_length=254)),
                ('email2', models.EmailField(default='', blank=True, max_length=254)),
                ('data_nascita', models.DateField(null=True, blank=True)),
                ('note', models.TextField(default='', blank=True)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('azienda', models.ForeignKey(to='aziende.Azienda')),
                ('categorie', models.ManyToManyField(to='aziende.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Nazioni',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nazione', models.CharField(unique=True, max_length=100)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provincie',
            fields=[
                ('provincia', models.CharField(unique=True, max_length=100)),
                ('sigla', models.CharField(primary_key=True, serialize=False, max_length=2)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='azienda',
            name='categorie',
            field=models.ManyToManyField(to='aziende.Categoria'),
        ),
        migrations.AddField(
            model_name='azienda',
            name='nazione',
            field=models.ForeignKey(to='aziende.Nazioni', default=181),
        ),
        migrations.AddField(
            model_name='azienda',
            name='provincia',
            field=models.ForeignKey(to='aziende.Provincie', default='TO'),
        ),
    ]
