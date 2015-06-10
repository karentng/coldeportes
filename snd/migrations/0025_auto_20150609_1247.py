# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0024_entrenador_sexo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrenador',
            name='altura',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='entrenador',
            name='correo_electronico',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='entrenador',
            name='foto',
            field=models.ImageField(upload_to='fotos_entrenadores', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entrenador',
            name='peso',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='entrenador',
            name='telefono_celular',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='entrenador',
            name='telefono_fijo',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='formaciondeportiva',
            name='nivel',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
