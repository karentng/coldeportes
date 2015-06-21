# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0036_entrenador_nacionalidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cacostouso',
            name='privado',
            field=models.PositiveIntegerField(verbose_name='Costo mensual al afiliado', default=0),
        ),
        migrations.AlterField(
            model_name='cacostouso',
            name='publico',
            field=models.PositiveIntegerField(verbose_name='Costo mensual al público', default=0),
        ),
        migrations.AlterField(
            model_name='centroacondicionamiento',
            name='telefono',
            field=models.CharField(verbose_name='teléfono', max_length=50),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='telefono',
            field=models.CharField(max_length=20),
        ),
    ]
