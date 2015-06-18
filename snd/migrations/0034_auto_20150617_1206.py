# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0008_tipodisciplinadeportiva'),
        ('snd', '0033_auto_20150617_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='deportista',
            name='disciplinas',
            field=models.ManyToManyField(to='entidades.TipoDisciplinaDeportiva'),
        ),
        migrations.AddField(
            model_name='formaciondeportiva',
            name='disciplina_deportiva',
            field=models.ManyToManyField(to='entidades.TipoDisciplinaDeportiva'),
        ),
    ]
