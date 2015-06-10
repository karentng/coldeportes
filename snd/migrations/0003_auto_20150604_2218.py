# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0003_tipousoescenario'),
        ('snd', '0002_auto_20150604_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caracterizacionescenario',
            name='clase_uso',
        ),
        migrations.AddField(
            model_name='caracterizacionescenario',
            name='clase_uso',
            field=models.ManyToManyField(to='entidades.TipoUsoEscenario'),
        ),
    ]
