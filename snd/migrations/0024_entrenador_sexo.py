# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0023_auto_20150609_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrenador',
            name='sexo',
            field=models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], max_length=11),
            preserve_default=False,
        ),
    ]
