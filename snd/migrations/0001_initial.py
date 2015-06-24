# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import snd.modelos.dirigentes


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CACostoUso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('privado', models.PositiveIntegerField(verbose_name='Costo mensual al afiliado', default=0)),
                ('publico', models.PositiveIntegerField(verbose_name='Costo mensual al público', default=0)),
                ('libre', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CAOtros',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('camerinos', models.BooleanField()),
                ('duchas', models.BooleanField()),
                ('comentarios', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CaracterizacionEscenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('capacidad_espectadores', models.CharField(max_length=50, verbose_name='capacidad de zona espectadores')),
                ('metros_construidos', models.CharField(max_length=50, verbose_name='metros cuadrados construídos')),
                ('tipo_superficie_juego', models.CharField(max_length=100, null=True)),
                ('clase_acceso', models.CharField(max_length=3, choices=[('pr', 'Privado'), ('dul', 'De Uso Libre'), ('pcp', 'Público Con Pago')], verbose_name='tipo de acceso')),
                ('descripcion', models.CharField(max_length=1024, verbose_name='descripción', null=True)),
                ('caracteristicas', models.ManyToManyField(to='entidades.CaracteristicaEscenario')),
                ('clase_uso', models.ManyToManyField(to='entidades.TipoUsoEscenario')),
            ],
        ),
        migrations.CreateModel(
            name='CAServicios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100, verbose_name='dirección')),
                ('telefono', models.CharField(max_length=50, verbose_name='teléfono')),
                ('email', models.EmailField(max_length=254)),
                ('latitud', models.FloatField(max_length=10)),
                ('longitud', models.FloatField(max_length=10)),
                ('altura', models.FloatField(max_length=10)),
                ('contacto', models.TextField(verbose_name='información de contacto', null=True, blank=True)),
                ('activo', models.BooleanField(default=True)),
                ('ciudad', models.ForeignKey(to='entidades.Ciudad')),
                ('entidad', models.ForeignKey(to='entidades.Entidad')),
            ],
        ),
        migrations.CreateModel(
            name='ComposicionCorporal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('peso', models.FloatField()),
                ('estatura', models.FloatField()),
                ('RH', models.CharField(max_length=4, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], default='O+')),
                ('talla_camisa', models.CharField(max_length=100)),
                ('talla_pantaloneta', models.CharField(max_length=100)),
                ('talla_zapato', models.CharField(max_length=100)),
                ('porcentaje_grasa', models.CharField(max_length=100)),
                ('porcentaje_musculo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='DatoHistorico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('descripcion', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Deportista',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('genero', models.CharField(max_length=11, choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')], default='Hombre', verbose_name='Genero del Deportista')),
                ('tipo_id', models.CharField(max_length=10, choices=[('TI', 'Tarjeta de Identidad'), ('CC', 'Cédula de ciudadanía'), ('CCEX', 'Cédula de extranjero'), ('PASS', 'Pasaporte')], default='CC', verbose_name='Tipo de Identificación')),
                ('identificacion', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('barrio', models.CharField(max_length=100)),
                ('comuna', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('telefono', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
                ('video', models.URLField(max_length=1024, verbose_name='Video', null=True, blank=True)),
                ('foto', models.ImageField(null=True, upload_to='fotos_deportistas', blank=True)),
                ('ciudad_nacimiento', models.ForeignKey(to='entidades.Ciudad', blank=True)),
                ('disciplinas', models.ManyToManyField(to='entidades.TipoDisciplinaDeportiva')),
                ('entidad', models.ForeignKey(to='entidades.Entidad')),
                ('nacionalidad', models.ManyToManyField(to='entidades.Nacionalidad')),
            ],
        ),
        migrations.CreateModel(
            name='Dirigente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('tipo_identificacion', models.CharField(max_length=2, choices=[('CC', 'Cédula de ciudadanía'), ('CE', 'Cédula de extranjería'), ('PT', 'Pasaporte')], verbose_name='Tipo de Identificación')),
                ('identificacion', models.CharField(max_length=20, verbose_name='Número de Identificación')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('genero', models.CharField(max_length=6, choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')], verbose_name='Género')),
                ('cargo', models.CharField(max_length=100, verbose_name='Nombre del Cargo')),
                ('telefono', models.CharField(max_length=100, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('fecha_posesion', models.DateField(verbose_name='Fecha de Posesión')),
                ('fecha_retiro', models.DateField(verbose_name='Fecha de Retiro', null=True, blank=True)),
                ('foto', models.ImageField(null=True, upload_to=snd.modelos.dirigentes.Dirigente.foto_name, blank=True)),
                ('activo', models.BooleanField(default=True)),
                ('descripcion', models.CharField(max_length=500, verbose_name='Descripción o Logros')),
                ('entidad', models.ForeignKey(null=True, to='entidades.Entidad', blank=True)),
                ('nacionalidad', models.ManyToManyField(to='entidades.Nacionalidad')),
                ('superior', models.ForeignKey(null=True, to='snd.Dirigente', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entrenador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('estado', models.BooleanField(choices=[('Activo', True), ('Inactivo', False)], default=True)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('genero', models.CharField(max_length=11, choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')])),
                ('foto', models.ImageField(null=True, upload_to='fotos_entrenadores', blank=True)),
                ('tipo_id', models.CharField(max_length=5, choices=[('CED', 'Cédula de ciudadanía'), ('CEDEX', 'Cédula de extranjero'), ('PAS', 'Pasaporte')], default='CED')),
                ('nro_id', models.BigIntegerField()),
                ('telefono_fijo', models.CharField(max_length=50, blank=True)),
                ('telefono_celular', models.CharField(max_length=50, blank=True)),
                ('correo_electronico', models.EmailField(max_length=254, blank=True)),
                ('fecha_nacimiento', models.DateField()),
                ('altura', models.IntegerField(blank=True)),
                ('peso', models.IntegerField(blank=True)),
                ('ciudad', models.ForeignKey(to='entidades.Ciudad', blank=True)),
                ('entidad_vinculacion', models.ForeignKey(to='entidades.Entidad')),
                ('nacionalidad', models.ManyToManyField(to='entidades.Nacionalidad')),
            ],
        ),
        migrations.CreateModel(
            name='Escenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('latitud', models.FloatField(max_length=10)),
                ('longitud', models.FloatField(max_length=10)),
                ('altura', models.FloatField(max_length=10)),
                ('comuna', models.CharField(max_length=10)),
                ('barrio', models.CharField(max_length=20)),
                ('estrato', models.CharField(max_length=1, choices=[('1', 'Uno'), ('2', 'Dos'), ('3', 'Tres'), ('4', 'Cuatro'), ('5', 'Cinco'), ('6', 'Seis')])),
                ('nombre_administrador', models.CharField(max_length=50, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('descripcion', models.CharField(max_length=1024, verbose_name='descripción', null=True)),
                ('ciudad', models.ForeignKey(to='entidades.Ciudad')),
                ('entidad', models.ForeignKey(to='entidades.Entidad')),
            ],
        ),
        migrations.CreateModel(
            name='ExperienciaLaboral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre_cargo', models.CharField(max_length=50)),
                ('institucion', models.CharField(max_length=150)),
                ('fecha_comienzo', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('entrenador', models.ForeignKey(to='snd.Entrenador')),
            ],
        ),
        migrations.CreateModel(
            name='FormacionDeportiva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('denominacion_diploma', models.CharField(max_length=150)),
                ('nivel', models.CharField(max_length=50, blank=True)),
                ('institucion_formacion', models.CharField(max_length=100)),
                ('fecha_comienzo', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('disciplina_deportiva', models.ManyToManyField(to='entidades.TipoDisciplinaDeportiva')),
                ('entrenador', models.ForeignKey(to='snd.Entrenador')),
                ('pais_formacion', models.ForeignKey(to='entidades.Nacionalidad')),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('foto', models.ImageField(null=True, upload_to='fotos_escenarios', blank=True)),
                ('escenario', models.ForeignKey(to='snd.Escenario')),
            ],
        ),
        migrations.CreateModel(
            name='Funcion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('descripcion', models.CharField(max_length=200, verbose_name='Descripción')),
                ('dirigente', models.ForeignKey(to='snd.Dirigente')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialDeportivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha', models.DateField()),
                ('lugar', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('institucion_equipo', models.CharField(max_length=100, null=True, blank=True)),
                ('tipo', models.CharField(max_length=100, choices=[('Competencia', 'Competencia'), ('Logro Deportivo', 'Logro Deportivo'), ('Participacion en Equipo', 'Participacion en Equipo'), ('Premio', 'Premio')], default='Competencia', verbose_name='Tipo Historial')),
                ('deportista', models.ForeignKey(to='snd.Deportista')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioDisponibilidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('descripcion', models.CharField(max_length=1024)),
                ('dias', models.ManyToManyField(to='entidades.Dias')),
                ('escenario', models.ForeignKey(to='snd.Escenario')),
            ],
        ),
        migrations.CreateModel(
            name='InformacionAcademica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('institucion', models.CharField(max_length=100)),
                ('nivel', models.CharField(max_length=20, choices=[('Jardin', 'Jardin'), ('Primaria', 'Primaria'), ('Bachillerato', 'Bachillerato'), ('Pregrado', 'Pregrado'), ('Postgrado', 'Postgrado')])),
                ('estado', models.CharField(max_length=20, choices=[('Actual', 'Actual'), ('Finalizado', 'Finalizado'), ('Incompleto', 'Incompleto')])),
                ('profesion', models.CharField(max_length=100, null=True, blank=True)),
                ('grado_semestre', models.IntegerField(verbose_name='Grado o Semestre', null=True, blank=True)),
                ('fecha_finalizacion', models.IntegerField(verbose_name='Año Finalización', null=True, blank=True)),
                ('deportista', models.ForeignKey(to='snd.Deportista')),
                ('pais', models.ForeignKey(to='entidades.Nacionalidad')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('url', models.CharField(max_length=1024, verbose_name='url', null=True)),
                ('descripcion', models.CharField(max_length=1024, null=True)),
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
            model_name='composicioncorporal',
            name='deportista',
            field=models.ForeignKey(to='snd.Deportista'),
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
            field=models.ManyToManyField(to='entidades.TipoDisciplinaDeportiva'),
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
