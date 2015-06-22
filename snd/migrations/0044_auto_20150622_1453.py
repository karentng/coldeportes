# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0043_auto_20150622_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deportista',
            name='tipo_id',
            field=models.CharField(max_length=10, choices=[('TI', 'Tarjeta de Identidad'), ('CC', 'Cédula de ciudadanía'), ('CCEX', 'Cédula de extranjero'), ('PASS', 'Pasaporte')], default='CC', verbose_name='Tipo de Identificación'),
        ),
    ]
