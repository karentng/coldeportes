# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0020_remove_informacionacademica_fecha_finalizacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='informacionacademica',
            name='fecha_finalizacion',
            field=models.IntegerField(verbose_name='Año Finalización', blank=True, null=True),
        ),
    ]
