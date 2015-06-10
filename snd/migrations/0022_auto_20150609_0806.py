# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0006_nacionalidad_iso'),
        ('snd', '0021_informacionacademica_fecha_finalizacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrenador',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('estado', models.BooleanField(default=True, choices=[('Activo', True), ('Inactivo', False)])),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('foto', models.ImageField(upload_to='')),
                ('tipo_id', models.CharField(default='CED', choices=[('CED', 'Cédula de ciudadanía'), ('CEDEX', 'Cédula de extranjero'), ('NIT', 'NIT')], max_length=5)),
                ('nro_id', models.BigIntegerField()),
                ('telefono_fijo', models.CharField(max_length=50)),
                ('telefono_celular', models.CharField(max_length=50)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('fecha_nacimiento', models.DateField()),
                ('altura', models.IntegerField()),
                ('peso', models.IntegerField()),
                ('ciudad', models.ForeignKey(blank=True, to='entidades.Ciudad')),
                ('entidad_vinculacion', models.ForeignKey(to='entidades.Entidad')),
            ],
        ),
        migrations.CreateModel(
            name='ExperienciaLaboral',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nombre_cargo', models.CharField(max_length=50)),
                ('institucion', models.CharField(max_length=150)),
                ('fecha_comienzo', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='FormacionDeportiva',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('denominacion_diploma', models.CharField(max_length=150)),
                ('nivel', models.CharField(max_length=50)),
                ('institucion_formacion', models.CharField(max_length=100)),
                ('fecha_comienzo', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('disciplina_deportiva', models.ForeignKey(to='entidades.DisciplinaDepostiva')),
                ('pais_formacion', models.ForeignKey(to='entidades.Nacionalidad')),
            ],
        ),
        migrations.AddField(
            model_name='entrenador',
            name='experiencia_laboral',
            field=models.ForeignKey(to='snd.ExperienciaLaboral'),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='formacion_deportiva',
            field=models.ForeignKey(to='snd.FormacionDeportiva'),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='nacionalidad',
            field=models.ForeignKey(to='entidades.Nacionalidad'),
        ),
    ]
