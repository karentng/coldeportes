# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [

    ]

    operations = [
        migrations.CreateModel(
            name='Transferencia',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('fecha_solicitud', models.DateField()),
                ('tipo_objeto', models.CharField(max_length=100)),
                ('id_objeto', models.IntegerField()),
                ('entidad', models.ForeignKey(to='entidades.Entidad')),
            ],
        ),
    ]
