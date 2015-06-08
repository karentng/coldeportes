# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0012_auto_20150607_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deportista',
            name='video',
            field=models.URLField(null=True, verbose_name='Video', max_length=1024),
        ),
    ]
