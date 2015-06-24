# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0041_auto_20150622_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composicioncorporal',
            name='RH',
            field=models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], default='O+', max_length=4),
        ),
        migrations.AlterField(
            model_name='historialdeportivo',
            name='tipo',
            field=models.CharField(choices=[('Competencia', 'Competencia'), ('Logro Deportivo', 'Logro Deportivo'), ('Participacion en Equipo', 'Participacion en Equipo'), ('Premio', 'Premio')], verbose_name='Tipo Historial', max_length=100, default='Competencia'),
        ),
        migrations.AlterField(
            model_name='informacionacademica',
            name='estado',
            field=models.CharField(choices=[('Actual', 'Actual'), ('Finalizado', 'Finalizado'), ('Incompleto', 'Incompleto')], max_length=20),
        ),
    ]
