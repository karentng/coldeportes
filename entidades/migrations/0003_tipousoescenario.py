# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0002_auto_20150521_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoUsoEscenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50, verbose_name='descripción')),
            ],
        ),
    ]
