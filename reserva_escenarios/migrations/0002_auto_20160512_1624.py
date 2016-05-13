# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reserva_escenarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservaescenario',
            name='nombre_equipo',
            field=models.CharField(verbose_name='nombre de grupo que utilizará el escenario', max_length=150, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservaescenario',
            name='direccion_solicitante',
            field=models.CharField(verbose_name='dirección', max_length=150),
        ),
        migrations.AlterField(
            model_name='reservaescenario',
            name='identificacion_solicitante',
            field=models.CharField(verbose_name='número de identificación', max_length=150),
        ),
        migrations.AlterField(
            model_name='reservaescenario',
            name='nombre_solicitante',
            field=models.CharField(verbose_name='nombre', max_length=150),
        ),
        migrations.AlterField(
            model_name='reservaescenario',
            name='telefono_solicitante',
            field=models.CharField(verbose_name='teléfono', max_length=150),
        ),
    ]
