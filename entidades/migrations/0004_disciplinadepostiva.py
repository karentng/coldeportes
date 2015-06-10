# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0003_tipousoescenario'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisciplinaDepostiva',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('descripcion', models.CharField(verbose_name='descripción', max_length=50)),
            ],
        ),
    ]
