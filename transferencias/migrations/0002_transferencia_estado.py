# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transferencias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferencia',
            name='estado',
            field=models.CharField(default='Pendiente', choices=[('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada')], max_length=20),
        ),
    ]
