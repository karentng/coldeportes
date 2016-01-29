# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manual', '0002_auto_20160128_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='subtitulo',
            field=models.CharField(max_length=100, verbose_name='subtítulo del artículo'),
        ),
    ]
