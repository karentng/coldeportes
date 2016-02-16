# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import registro_resultados.models


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0003_auto_20160214_0037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competencia',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nombre', models.CharField(verbose_name='nombre', max_length=255)),
                ('anno', models.PositiveIntegerField(verbose_name='año de la competencia')),
                ('tipos_participantes', models.IntegerField(verbose_name='tipo de participantes', choices=[(1, 'Individual'), (2, 'Equipos')])),
                ('tiempos', models.BooleanField(verbose_name='¿Requiere el registro de tiempos?')),
                ('imagen', models.FileField(verbose_name='imagen representativa de la competencia', upload_to=registro_resultados.models.ruta_competencias_imagenes, blank=True, null=True)),
                ('descripcion', models.TextField()),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('categorias', models.ManyToManyField(verbose_name='Seleccione todas las modalidades que estarán presentes en la competencia', to='entidades.CategoriaDisciplinaDeportiva')),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nombre', models.CharField(verbose_name='nombre', max_length=255)),
                ('posicion', models.IntegerField(default=0)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('competencia', models.ForeignKey(to='registro_resultados.Competencia')),
                ('departamento', models.ForeignKey(to='entidades.Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nombres', models.CharField(verbose_name='nombre', max_length=255)),
                ('apellidos', models.CharField(verbose_name='apellidos', max_length=255)),
                ('genero', models.CharField(verbose_name='Genero del Deportista', choices=[('HOMBRE', 'MASCULINO'), ('MUJER', 'FEMENINO')], max_length=11)),
                ('posicion', models.IntegerField(default=0)),
                ('tiempo', models.TimeField(null=True, blank=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('competencia', models.ForeignKey(blank=True, null=True, to='registro_resultados.Competencia')),
                ('departamento', models.ForeignKey(to='entidades.Departamento')),
                ('equipo', models.ForeignKey(blank=True, null=True, to='registro_resultados.Equipo')),
            ],
        ),
    ]
