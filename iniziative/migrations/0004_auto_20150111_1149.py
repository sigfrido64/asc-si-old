# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('iniziative', '0003_auto_20150111_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iniziativa',
            name='in_uso',
            field=models.BooleanField(default=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='iniziativa',
            name='nome',
            field=models.CharField(validators=[django.core.validators.MinLengthValidator(3)], max_length=80,
                                   unique=True, db_index=True, verbose_name='Nome Iniziativa'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='raggruppamento',
            name='in_uso',
            field=models.BooleanField(default=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='raggruppamento',
            name='nome',
            field=models.CharField(max_length=80, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sottoiniziativa',
            name='in_uso',
            field=models.BooleanField(default=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sottoiniziativa',
            name='nome',
            field=models.CharField(max_length=80, db_index=True),
            preserve_default=True,
        ),
    ]
