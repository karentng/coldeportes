# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0006_auto_20160408_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdjuntoSolicitud',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='adjuntos_adecuacion_escenarios', verbose_name='Archivo a adjuntar')),
            ],
        ),
        migrations.CreateModel(
            name='DiscucionSolicitud',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('estado_anterior', models.IntegerField(choices=[(0, 'ESPERANDO RESPUESTA'), (1, 'INCOMPLETA'), (2, 'APROBADA'), (3, 'RECHAZADA')])),
                ('estado_actual', models.IntegerField(choices=[(0, 'ESPERANDO RESPUESTA'), (1, 'INCOMPLETA'), (2, 'APROBADA'), (3, 'RECHAZADA')], verbose_name='Cambiar estado a')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('respuesta', models.BooleanField()),
                ('entidad', models.ForeignKey(to='entidades.Entidad')),
            ],
        ),
        migrations.CreateModel(
            name='ReconocimientoDeportivo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('estado', models.IntegerField(default=0, choices=[(0, 'ESPERANDO RESPUESTA'), (1, 'INCOMPLETA'), (2, 'APROBADA'), (3, 'ANULADA'), (4, 'CANCELADA POR ENTIDAD')])),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('nombre_solicitante', models.CharField(max_length=150, verbose_name='Nombre')),
                ('id_solicitante', models.CharField(max_length=150, verbose_name='Número de identificación')),
                ('tel_solicitante', models.CharField(max_length=150, verbose_name='Teléfono')),
                ('direccion_solicitante', models.CharField(max_length=150, verbose_name='Dirección')),
                ('vinculo_solicitante', models.IntegerField(choices=[(0, 'USUARIO EXTERNO'), (1, 'CONTRATISTA'), (2, 'FUNCIONARIO')], verbose_name='Vínculo con la entidad')),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('para_quien', models.ForeignKey(to='entidades.Entidad', verbose_name='Dirigido a')),
            ],
            options={
                'permissions': (('view_reconocimientodeportivo', 'Permite ver solicitudes de reconocimiento deportivo'),),
            },
        ),
        migrations.AddField(
            model_name='discucionsolicitud',
            name='solicitud',
            field=models.ForeignKey(to='reconocimiento_deportivo.ReconocimientoDeportivo'),
        ),
        migrations.AddField(
            model_name='adjuntosolicitud',
            name='discucion',
            field=models.ForeignKey(blank=True, to='reconocimiento_deportivo.DiscucionSolicitud', null=True),
        ),
        migrations.AddField(
            model_name='adjuntosolicitud',
            name='solicitud',
            field=models.ForeignKey(to='reconocimiento_deportivo.ReconocimientoDeportivo'),
        ),
    ]
