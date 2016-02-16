# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0003_auto_20160214_0037'),
        ('registro_resultados', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participante',
            name='categoria',
            field=models.ForeignKey(to='entidades.CategoriaDisciplinaDeportiva', default=1),
            preserve_default=False,
        ),
    ]
