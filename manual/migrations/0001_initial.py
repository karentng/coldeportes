# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('titulo', models.CharField(max_length=100, unique=True, verbose_name='título del artículo')),
                ('subtitulo', models.CharField(max_length=100, unique=True, verbose_name='subtítulo del artículo')),
                ('palabras_clave', models.CharField(max_length=1024, verbose_name='palabras clave')),
                ('imagen', models.FileField(upload_to='', verbose_name='imagen')),
                ('contenido', models.TextField()),
            ],
        ),
    ]
