# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0008_tipodisciplinadeportiva'),
        ('snd', '0039_remove_caracterizacionescenario_tipo_disciplinas'),
    ]

    operations = [
        migrations.AddField(
            model_name='caracterizacionescenario',
            name='tipo_disciplinas',
            field=models.ManyToManyField(to='entidades.TipoDisciplinaDeportiva'),
        ),
    ]
