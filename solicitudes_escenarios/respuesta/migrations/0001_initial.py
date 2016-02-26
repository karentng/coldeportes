# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0006_auto_20160219_0354'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaSolicitudes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('solicitud', models.PositiveIntegerField()),
                ('entidad_solicitante', models.ForeignKey(to='entidades.Entidad')),
            ],
        ),
    ]
