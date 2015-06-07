# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0005_nacionalidad'),
        ('snd', '0011_auto_20150607_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deportista',
            name='nacionalidad',
        ),
        migrations.AddField(
            model_name='deportista',
            name='nacionalidad',
            field=models.ManyToManyField(to='entidades.Nacionalidad'),
        ),
    ]
