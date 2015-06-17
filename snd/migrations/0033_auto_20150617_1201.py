# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0032_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deportista',
            name='disciplinas',
        ),
        migrations.RemoveField(
            model_name='formaciondeportiva',
            name='disciplina_deportiva',
        ),
    ]
