# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0007_deportista_disciplinas'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComposicionCorporal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('peso', models.FloatField()),
                ('estatura', models.IntegerField()),
                ('RH', models.CharField(max_length=100)),
                ('talla_camisa', models.CharField(max_length=100)),
                ('talla_pantaloneta', models.CharField(max_length=100)),
                ('talla_zapato', models.CharField(max_length=100)),
                ('porcentaje_grasa', models.CharField(max_length=100)),
                ('porcentaje_musculo', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='deportista',
            name='RH',
        ),
        migrations.RemoveField(
            model_name='deportista',
            name='estatura',
        ),
        migrations.RemoveField(
            model_name='deportista',
            name='nacionalidad',
        ),
        migrations.RemoveField(
            model_name='deportista',
            name='peso',
        ),
        migrations.RemoveField(
            model_name='deportista',
            name='porcentaje_grasa',
        ),
        migrations.RemoveField(
            model_name='deportista',
            name='porcentaje_musculo',
        ),
        migrations.RemoveField(
            model_name='deportista',
            name='talla_camisa',
        ),
        migrations.RemoveField(
            model_name='deportista',
            name='talla_pantaloneta',
        ),
        migrations.RemoveField(
            model_name='deportista',
            name='talla_zapato',
        ),
        migrations.AddField(
            model_name='deportista',
            name='foto',
            field=models.ImageField(null=True, blank=True, upload_to='fotos_deportistas'),
        ),
        migrations.AddField(
            model_name='deportista',
            name='video',
            field=models.CharField(null=True, verbose_name='url', max_length=1024),
        ),
        migrations.AddField(
            model_name='historialdeportivo',
            name='deportista',
            field=models.ForeignKey(to='snd.Deportista', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='informacionacademica',
            name='deportista',
            field=models.ForeignKey(to='snd.Deportista', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='representante',
            name='deportista',
            field=models.ForeignKey(to='snd.Deportista', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='composicioncorporal',
            name='deportista',
            field=models.ForeignKey(to='snd.Deportista'),
        ),
    ]
