# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0002_auto_20150521_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='CACostoUso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privado', models.PositiveIntegerField(default=0)),
                ('publico', models.PositiveIntegerField(verbose_name='público', default=0)),
                ('libre', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CAOtros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camerinos', models.BooleanField()),
                ('duchas', models.BooleanField()),
                ('comentarios', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CaracterizacionEscenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacidad_espectadores', models.CharField(verbose_name='capacidad de zona espectadores', max_length=50)),
                ('metros_construidos', models.CharField(verbose_name='metros cuadrados construídos', max_length=50)),
                ('tipo_superficie_juego', models.CharField(max_length=100, null=True)),
                ('clase_acceso', models.CharField(choices=[('pr', 'Privado'), ('dul', 'De Uso Libre'), ('pcp', 'Público Con Pago')], verbose_name='tipo de acceso', max_length=3)),
                ('clase_uso', models.CharField(choices=[('af', 'Aficionado'), ('ar', 'De Alto Rendimiento'), ('sp', 'Sólo Profesional')], verbose_name='clase de uso', max_length=2)),
                ('descripcion', models.CharField(verbose_name='descripción', max_length=250, null=True)),
                ('caracteristicas', models.ManyToManyField(to='entidades.CaracteristicaEscenario')),
            ],
        ),
        migrations.CreateModel(
            name='CAServicios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acondicionamiento', models.BooleanField()),
                ('fortalecimiento', models.BooleanField()),
                ('zona_cardio', models.BooleanField()),
                ('zona_humeda', models.BooleanField(verbose_name='zona húmeda')),
                ('medico', models.BooleanField(verbose_name='médico')),
                ('nutricionista', models.BooleanField()),
                ('fisioterapia', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CentroAcondicionamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(verbose_name='dirección', max_length=100)),
                ('telefono', models.BigIntegerField(verbose_name='teléfono')),
                ('email', models.EmailField(max_length=254)),
                ('latitud', models.FloatField(max_length=10)),
                ('longitud', models.FloatField(max_length=10)),
                ('altura', models.FloatField(max_length=10)),
                ('contacto', models.TextField(blank=True, verbose_name='información de contacto', null=True)),
                ('activo', models.BooleanField(default=True)),
                ('ciudad', models.ForeignKey(to='entidades.Ciudad')),
                ('entidad', models.ForeignKey(to='entidades.Entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('telefono', models.BigIntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='DatoHistorico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('descripcion', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Escenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('latitud', models.FloatField(max_length=10)),
                ('longitud', models.FloatField(max_length=10)),
                ('altura', models.FloatField(max_length=10)),
                ('comuna', models.CharField(max_length=10)),
                ('barrio', models.CharField(max_length=20)),
                ('estrato', models.CharField(choices=[('1', 'Uno'), ('2', 'Dos'), ('3', 'Tres'), ('4', 'Cuatro'), ('5', 'Cinco'), ('6', 'Seis')], max_length=1)),
                ('nombre_administrador', models.CharField(max_length=50, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('descripcion', models.CharField(verbose_name='descripción', max_length=250, null=True)),
                ('ciudad', models.ForeignKey(to='entidades.Ciudad')),
                ('entidad', models.ForeignKey(to='entidades.Entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, upload_to='fotos', null=True)),
                ('escenario', models.ForeignKey(to='snd.Escenario')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioDisponibilidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('descripcion', models.CharField(max_length=150)),
                ('dias', models.ManyToManyField(to='entidades.Dias')),
                ('escenario', models.ForeignKey(to='snd.Escenario')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, upload_to='videos', null=True)),
                ('escenario', models.ForeignKey(to='snd.Escenario')),
            ],
        ),
        migrations.AddField(
            model_name='datohistorico',
            name='escenario',
            field=models.ForeignKey(to='snd.Escenario'),
        ),
        migrations.AddField(
            model_name='contacto',
            name='escenario',
            field=models.ForeignKey(to='snd.Escenario'),
        ),
        migrations.AddField(
            model_name='caservicios',
            name='centro',
            field=models.OneToOneField(to='snd.CentroAcondicionamiento'),
        ),
        migrations.AddField(
            model_name='caracterizacionescenario',
            name='escenario',
            field=models.ForeignKey(to='snd.Escenario'),
        ),
        migrations.AddField(
            model_name='caracterizacionescenario',
            name='tipo_disciplinas',
            field=models.ManyToManyField(to='entidades.TipoDisciplinaEscenario'),
        ),
        migrations.AddField(
            model_name='caracterizacionescenario',
            name='tipo_escenario',
            field=models.ForeignKey(to='entidades.TipoEscenario'),
        ),
        migrations.AddField(
            model_name='caotros',
            name='centro',
            field=models.OneToOneField(to='snd.CentroAcondicionamiento'),
        ),
        migrations.AddField(
            model_name='cacostouso',
            name='centro',
            field=models.OneToOneField(to='snd.CentroAcondicionamiento'),
        ),
    ]
