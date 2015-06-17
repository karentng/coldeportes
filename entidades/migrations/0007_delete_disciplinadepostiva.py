# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0033_auto_20150617_1201'),
        ('entidades', '0006_nacionalidad_iso'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DisciplinaDepostiva',
        ),
    ]
