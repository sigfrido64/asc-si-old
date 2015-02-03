# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iniziative', '0002_auto_20150109_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='iniziativa',
            name='in_uso',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='raggruppamento',
            name='in_uso',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sottoiniziativa',
            name='in_uso',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
