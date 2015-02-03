# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nome', models.CharField(max_length=128)),
                ('sha1', models.CharField(max_length=128)),
                ('stato', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ordine',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('anno_formativo', models.CharField(max_length=10)),
                ('fornitore', models.PositiveIntegerField(default=0)),
                ('collaudo_funzionale', models.BooleanField(default=False)),
                ('data_ordine', models.DateTimeField()),
                ('data_consegna', models.DateTimeField()),
                ('destinazione', models.CharField(max_length=50)),
                ('tipologia_materiale', models.PositiveSmallIntegerField()),
                ('tipologia_iva', models.PositiveSmallIntegerField()),
                ('valore_iva', models.DecimalField(max_digits=3, decimal_places=3)),
                ('note', models.CharField(max_length=500)),
                ('valore_Ordine', models.DecimalField(max_digits=3, decimal_places=3)),
                ('ordine_completo', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
