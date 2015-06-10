# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0004_auto_20150604_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='descripcion',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
