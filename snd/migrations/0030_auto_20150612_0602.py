# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0029_auto_20150612_0450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dirigente',
            name='funciones',
        ),
        migrations.AddField(
            model_name='funcion',
            name='dirigente',
            field=models.ForeignKey(to='snd.Dirigente', default=''),
            preserve_default=False,
        ),
    ]
