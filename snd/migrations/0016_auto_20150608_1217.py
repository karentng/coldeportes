# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0015_auto_20150607_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialdeportivo',
            name='tipo',
            field=models.CharField(verbose_name='Tipo Historial', choices=[('Competencia', 'Competencia'), ('Premio', 'Premio'), ('Logro Deportivo', 'Logro Deportivo'), ('Participacion en Equipo', 'Participacion en Equipo')], max_length=100),
        ),
    ]
