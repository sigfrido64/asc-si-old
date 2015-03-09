# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import sifilesmanager.models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='INode',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=80)),
                ('descrizione', models.TextField(max_length=200)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('padre', models.ForeignKey(to='sifilesmanager.INode', blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiFile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=80)),
                ('descrizione', models.TextField(max_length=200)),
                ('sha1_hash', models.CharField(max_length=40, unique=True, db_index=True)),
                ('pathurl', models.CharField(max_length=2)),
                ('url', models.CharField(max_length=38)),
                ('filename', models.FileField(upload_to=sifilesmanager.models.upload_to_sha1, storage=django.core.files.storage.FileSystemStorage(location='C:\\Seafile\\Py\\si\\data'))),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('inode', models.ForeignKey(to='sifilesmanager.INode', default=None, null=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
