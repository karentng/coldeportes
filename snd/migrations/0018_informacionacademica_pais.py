# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0006_nacionalidad_iso'),
        ('snd', '0017_auto_20150608_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='informacionacademica',
            name='pais',
            field=models.ForeignKey(to='entidades.Nacionalidad', default='0'),
            preserve_default=False,
        ),
    ]
