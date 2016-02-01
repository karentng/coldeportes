# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manual', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='imagen',
            field=models.FileField(verbose_name='imagen', null=True, blank=True, upload_to=''),
        ),
    ]
