# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('corsi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('in_essere', models.BooleanField(default=False)),
                ('cognome', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('nome', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(3)])),
                ('codice_fiscale', models.CharField(max_length=16)),
                ('parametro', models.FloatField()),
                ('tipologia_fornitore', models.CharField(max_length=10)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IncaricoDocenza',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('data_inizio', models.DateField(auto_created=True)),
                ('data_proposta', models.DateField(auto_created=True)),
                ('proposta_numero', models.CharField(max_length=5)),
                ('data_fine', models.DateField()),
                ('descrizione', models.TextField(verbose_name='Descrizione Incarico', max_length=200)),
                ('ore_previste', models.IntegerField()),
                ('parametro', models.FloatField()),
                ('extra_compenso', models.FloatField(blank=True, default=0)),
                ('extra_compenso_motivazione', models.CharField(default='', blank=True, max_length=200)),
                ('compenso_totale_previsto', models.FloatField()),
                ('tipologia_fornitore', models.CharField(max_length=10)),
                ('iniziativa', models.CharField(max_length=20)),
                ('gruppo', models.CharField(max_length=20)),
                ('gruppo_sub1', models.CharField(max_length=20)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('codice_corso', models.ForeignKey(to='corsi.Corso')),
                ('docente', models.ForeignKey(to='docenti.Docente')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
