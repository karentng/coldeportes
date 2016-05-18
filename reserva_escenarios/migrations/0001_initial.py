# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservaEscenario',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateTimeField(null=True)),
                ('fecha_fin', models.DateTimeField(null=True)),
                ('nombre_equipo', models.CharField(max_length=150, verbose_name='nombre del grupo que utilizará el escenario')),
                ('nombre_solicitante', models.CharField(max_length=150, verbose_name='nombre del solicitante')),
                ('identificacion_solicitante', models.CharField(max_length=150, verbose_name='número de identificación del solicitante')),
                ('telefono_solicitante', models.CharField(max_length=150, verbose_name='teléfono de contacto')),
                ('direccion_solicitante', models.CharField(max_length=150, verbose_name='dirección de contacto')),
                ('descripcion', models.TextField(max_length=500, verbose_name='descripción de la actividad')),
                ('aprobada', models.BooleanField(default=False)),
                ('escenario', models.ForeignKey(to='snd.Escenario')),
            ],
        ),
    ]
