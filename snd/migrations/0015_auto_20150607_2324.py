# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0014_auto_20150607_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composicioncorporal',
            name='estatura',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='deportista',
            name='email',
            field=models.EmailField(null=True, blank=True, max_length=254),
        ),
    ]
