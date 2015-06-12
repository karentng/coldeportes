# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0006_nacionalidad_iso'),
        ('snd', '0028_auto_20150611_0952'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funcion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='dirigente',
            old_name='nombre',
            new_name='nombres',
        ),
        migrations.AddField(
            model_name='dirigente',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='dirigente',
            name='apellidos',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dirigente',
            name='descripcion',
            field=models.CharField(default='', max_length=500, verbose_name='Descripción o Logros'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dirigente',
            name='email',
            field=models.EmailField(null=True, max_length=254, blank=True),
        ),
        migrations.AddField(
            model_name='dirigente',
            name='fecha_posecion',
            field=models.DateField(default='2015-02-15'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dirigente',
            name='fecha_retiro',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dirigente',
            name='genero',
            field=models.CharField(choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')], default='', max_length=6, verbose_name='Género'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dirigente',
            name='identificacion',
            field=models.CharField(default='', max_length=20, verbose_name='Número de Identificación'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dirigente',
            name='nacionalidad',
            field=models.ManyToManyField(to='entidades.Nacionalidad'),
        ),
        migrations.AddField(
            model_name='dirigente',
            name='telefono',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dirigente',
            name='tipo_identificacion',
            field=models.CharField(choices=[('CC', 'Cédula de ciudadanía'), ('CE', 'Cédula de extranjería'), ('PT', 'Pasaporte')], default='', max_length=2, verbose_name='Tipo de Identificación'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dirigente',
            name='foto',
            field=models.ImageField(null=True, upload_to='fotos_dirigentes', blank=True),
        ),
        migrations.AddField(
            model_name='dirigente',
            name='funciones',
            field=models.ManyToManyField(to='snd.Funcion'),
        ),
    ]
