# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0022_auto_20150609_0806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrenador',
            name='experiencia_laboral',
        ),
        migrations.RemoveField(
            model_name='entrenador',
            name='formacion_deportiva',
        ),
        migrations.AddField(
            model_name='experiencialaboral',
            name='entrenador',
            field=models.ForeignKey(to='snd.Entrenador'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='formaciondeportiva',
            name='entrenador',
            field=models.ForeignKey(to='snd.Entrenador'),
            preserve_default=False,
        ),
    ]
