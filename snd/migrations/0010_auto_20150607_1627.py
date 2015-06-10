# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0009_remove_deportista_departamento_nacimiento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='representante',
            old_name='relación',
            new_name='relacion',
        ),
        migrations.AlterField(
            model_name='composicioncorporal',
            name='RH',
            field=models.CharField(max_length=4, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')]),
        ),
        migrations.AlterField(
            model_name='deportista',
            name='video',
            field=models.URLField(verbose_name='url', max_length=1024, null=True),
        ),
    ]
