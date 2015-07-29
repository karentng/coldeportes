# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CAFView',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EscenarioView',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('latitud', models.FloatField(max_length=10)),
                ('longitud', models.FloatField(max_length=10)),
                ('altura', models.FloatField(max_length=10)),
                ('comuna', models.CharField(max_length=10)),
                ('barrio', models.CharField(max_length=20)),
                ('estrato', models.CharField(max_length=1)),
                ('nombre_administrador', models.CharField(null=True, max_length=50)),
                ('estado', models.IntegerField()),
                ('nombre_contacto', models.CharField(max_length=50)),
                ('telefono_contacto', models.CharField(max_length=20)),
                ('email_contacto', models.EmailField(max_length=254)),
                ('descripcion_contacto', models.CharField(null=True, max_length=1024)),
                ('horario_id', models.IntegerField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('descripcion_horario', models.CharField(max_length=1024)),
                ('foto', models.ImageField(null=True, upload_to='fotos_escenarios', blank=True)),
                ('contenido', models.TextField()),
            ],
            options={
                'managed': False,
            },
        ),
    ]
