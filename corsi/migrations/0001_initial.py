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
                ('codice', models.CharField(validators=[django.core.validators.MinLengthValidator(6)], primary_key=True, serialize=False, max_length=10)),
                ('denominazione', models.CharField(validators=[django.core.validators.MinLengthValidator(5)], max_length=100)),
                ('data_inizio', models.DateField()),
                ('data_fine', models.DateField()),
                ('durata', models.IntegerField(default=8)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('raggruppamento', models.ForeignKey(to='iniziative.Raggruppamento')),
            ],
            options={
                'verbose_name_plural': 'Corsi',
                'verbose_name': 'Corso',
            },
            bases=(models.Model,),
        ),
    ]
