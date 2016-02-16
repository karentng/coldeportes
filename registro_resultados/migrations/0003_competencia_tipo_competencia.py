# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro_resultados', '0002_participante_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='competencia',
            name='tipo_competencia',
            field=models.IntegerField(default=1, choices=[(1, 'Olímpica'), (2, 'Paralímpica')], verbose_name='tipo de competencia'),
            preserve_default=False,
        ),
    ]
