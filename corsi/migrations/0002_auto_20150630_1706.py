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
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('inizio', models.DateTimeField()),
                ('fine', models.DateTimeField()),
                ('durata', models.FloatField()),
                ('anno', models.IntegerField()),
                ('doy', models.IntegerField()),
                ('tipologia', models.IntegerField(default=0, choices=[(0, 'Normale'), (0, 'Recupero')])),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('corso', models.ForeignKey(to='corsi.Corso')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='corso',
            name='denominazione',
            field=models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(10)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='corso',
            name='stato',
            field=models.IntegerField(default=0, choices=[(0, 'Bozza'), (10, 'Pianificato')]),
            preserve_default=True,
        ),
    ]
