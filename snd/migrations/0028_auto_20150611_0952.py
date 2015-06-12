# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0027_auto_20150609_2359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrenador',
            name='sexo',
        ),
        migrations.AddField(
            model_name='entrenador',
            name='genero',
            field=models.CharField(choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')], max_length=11),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entrenador',
            name='tipo_id',
            field=models.CharField(choices=[('CED', 'Cédula de ciudadanía'), ('CEDEX', 'Cédula de extranjero')], max_length=5, default='CED'),
        ),
    ]
