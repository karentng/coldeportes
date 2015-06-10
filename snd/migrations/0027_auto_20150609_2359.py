# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0006_nacionalidad_iso'),
        ('snd', '0026_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='dirigente',
            name='entidad',
            field=models.ForeignKey(null=True, to='entidades.Entidad', blank=True),
        ),
        migrations.AlterField(
            model_name='dirigente',
            name='superior',
            field=models.ForeignKey(null=True, to='snd.Dirigente', blank=True),
        ),
        migrations.AlterField(
            model_name='foto',
            name='foto',
            field=models.ImageField(upload_to='fotos_escenarios', null=True, blank=True),
        ),
    ]
