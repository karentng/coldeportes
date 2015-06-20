# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0029_auto_20150616_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deportista',
            name='genero',
            field=models.CharField(max_length=11, choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')], verbose_name='Genero del Deportista'),
        ),
    ]
