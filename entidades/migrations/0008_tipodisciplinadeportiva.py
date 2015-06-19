# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0007_delete_disciplinadepostiva'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDisciplinaDeportiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('descripcion', models.CharField(verbose_name='descripción', max_length=50)),
            ],
        ),
    ]
