# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0008_auto_20150607_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deportista',
            name='departamento_nacimiento',
        ),
    ]
