# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0040_caracterizacionescenario_tipo_disciplinas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='centroacondicionamiento',
            name='activo',
        ),
    ]
