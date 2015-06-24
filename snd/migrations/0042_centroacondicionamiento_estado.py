# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0041_remove_centroacondicionamiento_activo'),
    ]

    operations = [
        migrations.AddField(
            model_name='centroacondicionamiento',
            name='estado',
            field=models.IntegerField(default=1, choices=[(1, 'Activo'), (2, 'Inactivo')]),
        ),
    ]
