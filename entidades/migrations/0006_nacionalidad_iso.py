# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0005_nacionalidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='nacionalidad',
            name='iso',
            field=models.CharField(max_length=5, verbose_name='Abreviacion', default='CO'),
            preserve_default=False,
        ),
    ]
