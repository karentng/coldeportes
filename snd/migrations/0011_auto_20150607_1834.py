# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0005_nacionalidad'),
        ('snd', '0010_auto_20150607_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alergia',
            name='deportista',
        ),
        migrations.RemoveField(
            model_name='enfermedades',
            name='deportista',
        ),
        migrations.RemoveField(
            model_name='lesion',
            name='deportista',
        ),
        migrations.RemoveField(
            model_name='representante',
            name='deportista',
        ),
        migrations.RemoveField(
            model_name='seguromedico',
            name='deportista',
        ),
        migrations.AddField(
            model_name='deportista',
            name='nacionalidad',
            field=models.ForeignKey(to='entidades.Nacionalidad', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deportista',
            name='ciudad_nacimiento',
            field=models.ForeignKey(to='entidades.Ciudad', blank=True),
        ),
        migrations.DeleteModel(
            name='Alergia',
        ),
        migrations.DeleteModel(
            name='Enfermedades',
        ),
        migrations.DeleteModel(
            name='Lesion',
        ),
        migrations.DeleteModel(
            name='Representante',
        ),
        migrations.DeleteModel(
            name='SeguroMedico',
        ),
    ]
