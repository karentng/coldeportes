# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0004_disciplinadepostiva'),
        ('snd', '0005_video_descripcion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alergia',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('causa', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Deportista',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('sexo', models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], verbose_name='Sexo del Deportista', max_length=11)),
                ('identificacion', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('nacionalidad', models.CharField(max_length=100)),
                ('barrio', models.CharField(max_length=100)),
                ('comuna', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('peso', models.FloatField()),
                ('estatura', models.IntegerField()),
                ('RH', models.CharField(max_length=100)),
                ('talla_camisa', models.CharField(max_length=100)),
                ('talla_pantaloneta', models.CharField(max_length=100)),
                ('talla_zapato', models.CharField(max_length=100)),
                ('porcentaje_grasa', models.CharField(max_length=100)),
                ('porcentaje_musculo', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
                ('ciudad_nacimiento', models.ForeignKey(to='entidades.Ciudad')),
                ('departamento_nacimiento', models.ForeignKey(to='entidades.Departamento')),
                ('entidad', models.ForeignKey(to='entidades.Entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Enfermedades',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descipcion', models.TextField()),
                ('deportista', models.ForeignKey(to='snd.Deportista')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialDeportivo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('fecha', models.DateField()),
                ('lugar', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('institucion_equipo', models.CharField(blank=True, max_length=100, null=True)),
                ('tipo', models.CharField(choices=[('comp', 'Competencia'), ('premio', 'Premio'), ('logo_de', 'Logro Deportivo'), ('part', 'Participacion en Equipo')], verbose_name='Tipo Historial', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='InformacionAcademica',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('pais', models.CharField(max_length=100)),
                ('departamento', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=100)),
                ('institucion', models.CharField(max_length=100)),
                ('nivel', models.CharField(choices=[('Jardin', 'Jardin'), ('Primaria', 'Primaria'), ('Bachillerato', 'Bachillerato'), ('Pregrado', 'Pregrado'), ('Postgrado', 'Postgrado')], max_length=20)),
                ('grado_semestre', models.IntegerField()),
                ('profesion', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.CharField(choices=[('Finalizado', 'Finalizado'), ('Incompleto', 'Incompleto'), ('Actual', 'Actual')], max_length=20)),
                ('fecha_finalizacion', models.DateField(blank=True, null=True)),
                ('fecha_desercion', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lesion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('lugar', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('deportista', models.ForeignKey(to='snd.Deportista')),
            ],
        ),
        migrations.CreateModel(
            name='Representante',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('cedula_nit', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('relación', models.CharField(choices=[('fam', 'Familiar'), ('patr', 'Patrocinador'), ('contr', 'Contratado')], verbose_name='Representante del Deportista', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SeguroMedico',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('SISBEN', 'SISBEN'), ('EPS', 'EPS'), ('Medicina Prepagada', 'Medicina Prepagada')], max_length=10)),
                ('deportista', models.ForeignKey(to='snd.Deportista')),
            ],
        ),
        migrations.AddField(
            model_name='alergia',
            name='deportista',
            field=models.ForeignKey(to='snd.Deportista'),
        ),
    ]
