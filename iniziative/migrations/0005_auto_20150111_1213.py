# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iniziative', '0004_auto_20150111_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iniziativa',
            name='in_uso',
            field=models.BooleanField(db_index=True, verbose_name='In Uso', default=True),
            preserve_default=True,
        ),
    ]
