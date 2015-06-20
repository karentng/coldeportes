# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0008_tipodisciplinadeportiva'),
        ('snd', '0035_auto_20150617_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrenador',
            name='nacionalidad',
            field=models.ManyToManyField(to='entidades.Nacionalidad'),
        ),
    ]
