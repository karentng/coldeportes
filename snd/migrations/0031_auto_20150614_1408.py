# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0030_auto_20150612_0602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dirigente',
            name='cargo',
            field=models.CharField(max_length=100, verbose_name='Nombre del Cargo'),
        ),
        migrations.AlterField(
            model_name='dirigente',
            name='fecha_posecion',
            field=models.DateField(verbose_name='Fecha de Poseción'),
        ),
        migrations.AlterField(
            model_name='dirigente',
            name='fecha_retiro',
            field=models.DateField(verbose_name='Fecha de Retiro', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dirigente',
            name='telefono',
            field=models.CharField(max_length=100, verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='funcion',
            name='descripcion',
            field=models.CharField(max_length=200, verbose_name='Descripción'),
        ),
    ]
