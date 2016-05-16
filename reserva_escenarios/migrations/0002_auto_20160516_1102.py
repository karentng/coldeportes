# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reserva_escenarios', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservaescenario',
            name='escenario',
        ),
        migrations.DeleteModel(
            name='ReservaEscenario',
        ),
    ]
