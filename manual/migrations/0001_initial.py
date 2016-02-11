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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(unique=True, max_length=100, verbose_name='título del artículo')),
                ('orden', models.FloatField()),
                ('subtitulo', models.CharField(max_length=100, verbose_name='subtítulo del artículo')),
                ('palabras_clave', models.CharField(max_length=1024, verbose_name='palabras clave')),
                ('imagen', models.FileField(null=True, blank=True, upload_to='', verbose_name='imagen')),
                ('contenido', models.TextField()),
                ('modulo', models.CharField(choices=[('CF', 'CAFs'), ('CC', 'Caja de Compensaciones'), ('DE', 'Deportistas'), ('DR', 'Directorio'), ('DI', 'Dirigentes'), ('ES', 'Escenarios'), ('EC', 'Escuelas'), ('NO', 'Normograma'), ('NT', 'Noticias'), ('PA', 'Personal de Apoyo'), ('TR', 'Transferencias')], max_length=2)),
            ],
        ),
    ]
