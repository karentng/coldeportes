# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0016_auto_20150608_1217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informacionacademica',
            name='ciudad',
        ),
        migrations.RemoveField(
            model_name='informacionacademica',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='informacionacademica',
            name='pais',
        ),
        migrations.AlterField(
            model_name='informacionacademica',
            name='grado_semestre',
            field=models.IntegerField(null=True, verbose_name='Grado o Semestre', blank=True),
        ),
    ]
