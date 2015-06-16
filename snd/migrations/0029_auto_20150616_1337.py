# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0028_auto_20150611_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deportista',
            name='sexo',
        ),
        migrations.AddField(
            model_name='deportista',
            name='genero',
            field=models.CharField(default='Hombre', verbose_name='Genero del Deportista', max_length=11, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')]),
            preserve_default=False,
        ),
    ]
