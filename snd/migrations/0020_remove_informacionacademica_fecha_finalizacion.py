# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0019_remove_informacionacademica_fecha_desercion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informacionacademica',
            name='fecha_finalizacion',
        ),
    ]
