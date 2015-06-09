# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caracterizacionescenario',
            name='descripcion',
            field=models.CharField(null=True, max_length=1024, verbose_name='descripción'),
        ),
        migrations.AlterField(
            model_name='datohistorico',
            name='descripcion',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='escenario',
            name='descripcion',
            field=models.CharField(null=True, max_length=1024, verbose_name='descripción'),
        ),
        migrations.AlterField(
            model_name='horariodisponibilidad',
            name='descripcion',
            field=models.CharField(max_length=1024),
        ),
    ]
