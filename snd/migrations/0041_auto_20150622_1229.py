# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snd', '0040_caracterizacionescenario_tipo_disciplinas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deportista',
            name='genero',
            field=models.CharField(max_length=11, verbose_name='Genero del Deportista', choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')], default='Hombre'),
        ),
    ]
