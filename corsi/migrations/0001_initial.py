# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('iniziative', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corso',
            fields=[
                ('codice_edizione', models.CharField(serialize=False, validators=[django.core.validators.MinLengthValidator(6)], primary_key=True, max_length=10)),
                ('denominazione', models.CharField(validators=[django.core.validators.MinLengthValidator(5)], max_length=150)),
                ('data_inizio', models.DateField()),
                ('data_fine', models.DateField()),
                ('durata', models.IntegerField(default=8)),
                ('stato', models.IntegerField(choices=[(0, 'Bozza'), (10, 'Pianificato')])),
                ('note', models.CharField(max_length=1000)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('raggruppamento', models.ForeignKey(to='iniziative.Raggruppamento')),
            ],
            options={
                'verbose_name_plural': 'Corsi',
                'verbose_name': 'Corso',
            },
            bases=(models.Model,),
        ),
    ]
