# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0013_auto_20150607_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deportista',
            name='video',
            field=models.URLField(max_length=1024, verbose_name='Video', null=True, blank=True),
        ),
    ]
