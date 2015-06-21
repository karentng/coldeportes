# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import snd.modelos.dirigentes


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0037_auto_20150620_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dirigente',
            name='fecha_posecion',
        ),
        migrations.AddField(
            model_name='dirigente',
            name='fecha_posesion',
            field=models.DateField(default=datetime.datetime(2015, 6, 20, 20, 51, 16, 552052), verbose_name='Fecha de Posesión'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dirigente',
            name='foto',
            field=models.ImageField(blank=True, upload_to=snd.modelos.dirigentes.Dirigente.foto_name, null=True),
        ),
    ]
