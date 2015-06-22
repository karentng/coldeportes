# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0038_auto_20150620_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caracterizacionescenario',
            name='tipo_disciplinas',
        ),
    ]
