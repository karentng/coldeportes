# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0005_dirigenteformacionacademica'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservaEscenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('fecha_inicio', models.DateTimeField(null=True)),
                ('fecha_fin', models.DateTimeField(null=True)),
                ('decripcion', models.TextField(max_length=500, verbose_name='descripción')),
                ('nombre_equipo', models.CharField(max_length=150, verbose_name='nombre de grupo que utilizará el escenario')),
                ('nombre_solicitante', models.CharField(max_length=150, verbose_name='nombre')),
                ('identificacion_solicitante', models.CharField(max_length=150, verbose_name='número de identificación')),
                ('telefono_solicitante', models.CharField(max_length=150, verbose_name='teléfono')),
                ('direccion_solicitante', models.CharField(max_length=150, verbose_name='dirección')),
                ('aprobada', models.BooleanField(default=False)),
                ('escenario', models.ForeignKey(to='snd.Escenario')),
            ],
        ),
    ]
