# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('iniziative', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iniziativa',
            name='descrizione',
            field=models.CharField(verbose_name='Descrizione', max_length=80,
                                   validators=[django.core.validators.MinLengthValidator(5)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='iniziativa',
            name='nome',
            field=models.CharField(verbose_name='Nome Iniziativa', max_length=80, unique=True,
                                   validators=[django.core.validators.MinLengthValidator(3)]),
            preserve_default=True,
        ),
    ]
