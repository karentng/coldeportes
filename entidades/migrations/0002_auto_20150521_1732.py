# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaracteristicaEscenario',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50, verbose_name='descripción')),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre')),
                ('codigo', models.CharField(max_length=10, verbose_name='código', null=True)),
                ('latitud', models.FloatField(null=True)),
                ('longitud', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre')),
                ('codigo', models.CharField(max_length=10, verbose_name='código', null=True)),
                ('latitud', models.FloatField(null=True)),
                ('longitud', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dias',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TipoDisciplinaEscenario',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50, verbose_name='descripción')),
            ],
        ),
        migrations.CreateModel(
            name='TipoEscenario',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50, verbose_name='descripción')),
            ],
        ),
        migrations.AddField(
            model_name='ciudad',
            name='departamento',
            field=models.ForeignKey(to='entidades.Departamento'),
        ),
    ]
