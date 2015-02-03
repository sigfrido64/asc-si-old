# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iniziative', '0005_auto_20150111_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='raggruppamento',
            name='ordine',
            field=models.CharField(default='Ciao', max_length=10),
            preserve_default=False,
        ),
    ]
