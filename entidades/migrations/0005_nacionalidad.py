# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0004_disciplinadepostiva'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nacionalidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='pais', max_length=255)),
            ],
        ),
    ]
