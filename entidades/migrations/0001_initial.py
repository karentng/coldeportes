# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tenant_schemas.postgresql_backend.base


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaracteristicaEscenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('descripcion', models.CharField(max_length=50, verbose_name='descripción')),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre')),
                ('codigo', models.CharField(null=True, verbose_name='código', max_length=10)),
                ('latitud', models.FloatField(null=True)),
                ('longitud', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre')),
                ('codigo', models.CharField(null=True, verbose_name='código', max_length=10)),
                ('latitud', models.FloatField(null=True)),
                ('longitud', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nombre', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('domain_url', models.CharField(unique=True, max_length=128)),
                ('schema_name', models.CharField(unique=True, validators=[tenant_schemas.postgresql_backend.base._check_schema_name], max_length=63)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Nacionalidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('iso', models.CharField(max_length=5, verbose_name='Abreviacion')),
                ('nombre', models.CharField(max_length=255, verbose_name='pais')),
            ],
        ),
        migrations.CreateModel(
            name='TipoDisciplinaDeportiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('descripcion', models.CharField(max_length=50, verbose_name='descripción')),
            ],
        ),
        migrations.CreateModel(
            name='TipoDisciplinaEscenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('descripcion', models.CharField(max_length=50, verbose_name='descripción')),
            ],
        ),
        migrations.CreateModel(
            name='TipoEscenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('descripcion', models.CharField(max_length=50, verbose_name='descripción')),
            ],
        ),
        migrations.CreateModel(
            name='TipoUsoEscenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('descripcion', models.CharField(max_length=50, verbose_name='descripción')),
            ],
        ),
        migrations.AddField(
            model_name='ciudad',
            name='departamento',
            field=models.ForeignKey(to='entidades.Departamento'),
        ),
    ]
