# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0002_dirigenteformacionacademica'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservaEscenario',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('decripcion', models.TextField(verbose_name='descripción', max_length=500)),
                ('nombre_solicitante', models.CharField(verbose_name='Nombre', max_length=150)),
                ('identificacion_solicitante', models.CharField(verbose_name='Número de identificación', max_length=150)),
                ('telefono_solicitante', models.CharField(verbose_name='Teléfono', max_length=150)),
                ('direccion_solicitante', models.CharField(verbose_name='Dirección', max_length=150)),
                ('aprobada', models.BooleanField(default=False)),
                ('escenario', models.ForeignKey(to='snd.Escenario')),
            ],
        ),
    ]
