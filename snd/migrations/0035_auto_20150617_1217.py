# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0034_auto_20150617_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrenador',
            name='nacionalidad',
        ),
        migrations.AddField(
            model_name='deportista',
            name='tipo_id',
            field=models.CharField(default='CED', verbose_name='Tipo de Identificación', max_length=10, choices=[('TI', 'Tarjeta de Identidad'), ('CED', 'Cédula de ciudadanía'), ('CEDEX', 'Cédula de extranjero'), ('PAS', 'Pasaporte')]),
        ),
        migrations.AlterField(
            model_name='entrenador',
            name='tipo_id',
            field=models.CharField(default='CED', max_length=5, choices=[('CED', 'Cédula de ciudadanía'), ('CEDEX', 'Cédula de extranjero'), ('PAS', 'Pasaporte')]),
        ),
    ]
