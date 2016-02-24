# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0006_auto_20160219_0354'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdjuntoSolicitud',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='solicitudes_escenarios')),
            ],
        ),
        migrations.CreateModel(
            name='DiscucionSolicitud',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('estado_anterior', models.IntegerField(choices=[(0, 'ESPERANDO RESPUESTA'), (1, 'INCOMPLETA'), (2, 'APROBADA'), (3, 'ANULADA')])),
                ('estado_actual', models.IntegerField(choices=[(0, 'ESPERANDO RESPUESTA'), (1, 'INCOMPLETA'), (2, 'APROBADA'), (3, 'ANULADA')])),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudEscenario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(0, 'INFRAESTRUCTURA')])),
                ('prioridad', models.IntegerField(choices=[(0, 'BAJA'), (1, 'MEDIA'), (2, 'ALTA')])),
                ('descripcion', models.TextField()),
                ('escenarios', models.ManyToManyField(to='snd.Escenario')),
                ('para_quien', models.ForeignKey(to='entidades.Entidad')),
            ],
        ),
        migrations.AddField(
            model_name='discucionsolicitud',
            name='solicitud',
            field=models.ForeignKey(to='solicitud.SolicitudEscenario'),
        ),
        migrations.AddField(
            model_name='adjuntosolicitud',
            name='solicitud',
            field=models.ForeignKey(to='solicitud.SolicitudEscenario'),
        ),
    ]
