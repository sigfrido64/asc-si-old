# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Iniziativa',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nome', models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(3)],
                                          unique=True)),
                ('descrizione', models.CharField(max_length=80,
                                                 validators=[django.core.validators.MinLengthValidator(5)])),
                ('cup_cig', models.CharField(blank=True, verbose_name='CIG/CUP', max_length=80)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_tablespace': 'pippo',
                'verbose_name': 'Iniziativa',
                'verbose_name_plural': 'Iniziative',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Raggruppamento',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nome', models.CharField(max_length=80)),
                ('descrizione', models.CharField(max_length=80)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Raggruppamento',
                'verbose_name_plural': 'Raggruppamenti',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SottoIniziativa',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nome', models.CharField(max_length=80)),
                ('descrizione', models.CharField(max_length=80)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('iniziativa', models.ForeignKey(to='iniziative.Iniziativa')),
            ],
            options={
                'verbose_name': 'Sotto Iniziativa',
                'verbose_name_plural': 'Sotto Iniziative',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='raggruppamento',
            name='sotto_iniziativa',
            field=models.ForeignKey(to='iniziative.SottoIniziativa'),
            preserve_default=True,
        ),
    ]
