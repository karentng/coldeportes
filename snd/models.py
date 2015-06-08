#encoding:utf-8
from django.db import models
from entidades.models import *


# Create your models here.

class Escenario(models.Model):
    estratos = (('1', 'Uno'),
                ('2', 'Dos'),
                ('3', 'Tres'),
                ('4', 'Cuatro'),
                ('5', 'Cinco'),
                ('6', 'Seis'),
    )
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    latitud = models.FloatField(max_length=10)
    longitud = models.FloatField(max_length=10)
    altura = models.FloatField(max_length=10)
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.CharField(max_length=10)
    barrio = models.CharField(max_length=20)
    estrato = models.CharField(choices=estratos, max_length=1)
    nombre_administrador = models.CharField(max_length=50, null=True)
    entidad = models.ForeignKey(Entidad)    
    activo = models.BooleanField(default=True)
    descripcion = models.CharField(max_length=1024, verbose_name='descripción', null=True)

class CaracterizacionEscenario(models.Model):   
    accesos = (('pr', 'Privado'),
                ('dul', 'De Uso Libre'),
                ('pcp', 'Público Con Pago'),
    )
    escenario = models.ForeignKey(Escenario)
    capacidad_espectadores = models.CharField(max_length=50, verbose_name='capacidad de zona espectadores')
    metros_construidos = models.CharField(max_length=50, verbose_name='metros cuadrados construídos')
    tipo_escenario = models.ForeignKey(TipoEscenario)
    tipo_disciplinas = models.ManyToManyField(TipoDisciplinaEscenario)
    tipo_superficie_juego = models.CharField(max_length=100, null=True)
    clase_acceso = models.CharField(choices=accesos, max_length=3, verbose_name='tipo de acceso')
    caracteristicas = models.ManyToManyField(CaracteristicaEscenario)
    clase_uso = models.ManyToManyField(TipoUsoEscenario)
    descripcion = models.CharField(max_length=1024, verbose_name='descripción', null=True)

    

class HorarioDisponibilidad(models.Model):
    escenario = models.ForeignKey(Escenario)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dias = models.ManyToManyField(Dias)
    descripcion = models.CharField(max_length=1024)

class Foto(models.Model):
    escenario = models.ForeignKey(Escenario)
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)

class Video(models.Model):
    escenario = models.ForeignKey(Escenario)
    url = models.CharField(max_length=1024, verbose_name='url', null=True)
    descripcion = models.CharField(max_length=1024, null=True)

class DatoHistorico(models.Model):
    escenario = models.ForeignKey(Escenario)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.CharField(max_length=1024)

class Contacto(models.Model):
    escenario = models.ForeignKey(Escenario)
    nombre =  models.CharField(max_length=50)
    telefono = models.BigIntegerField()
    email = models.EmailField()

# Centro de Acondicionamiento Físico

class CentroAcondicionamiento(models.Model):
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, verbose_name="dirección")
    telefono = models.BigIntegerField(verbose_name="teléfono")
    email = models.EmailField()

    latitud = models.FloatField(max_length=10)
    longitud = models.FloatField(max_length=10)
    altura = models.FloatField(max_length=10)

    ciudad = models.ForeignKey(Ciudad)

    contacto = models.TextField(verbose_name='información de contacto', null=True, blank=True)

    entidad = models.ForeignKey(Entidad)    
    activo = models.BooleanField(default=True)

class CACostoUso(models.Model):
    centro = models.OneToOneField(CentroAcondicionamiento)
    privado = models.PositiveIntegerField(default=0)
    publico = models.PositiveIntegerField(verbose_name="público", default=0)
    libre = models.BooleanField()

class CAServicios(models.Model):
    centro = models.OneToOneField(CentroAcondicionamiento)
    acondicionamiento = models.BooleanField()
    fortalecimiento = models.BooleanField()
    zona_cardio = models.BooleanField()
    zona_humeda = models.BooleanField(verbose_name="zona húmeda")
    medico = models.BooleanField(verbose_name="médico")
    nutricionista = models.BooleanField()
    fisioterapia = models.BooleanField()

class CAOtros(models.Model):
    centro = models.OneToOneField(CentroAcondicionamiento)
    camerinos = models.BooleanField()
    duchas = models.BooleanField()
    comentarios = models.TextField(blank=True, null=True)

#Modelos de deportistas
#Informacion del deportista, informacion deportiva

class Deportista(models.Model):
    #Datos personales
        #Identificacion
    tipo_sexo = (
        ('Masculino','Masculino'),
        ('Femenino','Femenino'),
    )
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    sexo = models.CharField(choices=tipo_sexo,max_length=11, verbose_name='Sexo del Deportista')
    identificacion = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.ManyToManyField(Nacionalidad)
    ciudad_nacimiento = models.ForeignKey(Ciudad,blank=True)
    barrio = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    telefono = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
        #Entidad
    entidad = models.ForeignKey(Entidad)
        #Disciplina
    disciplinas = models.ManyToManyField(DisciplinaDepostiva)
    activo = models.BooleanField(default=True)
    video = models.URLField(max_length=1024, verbose_name='Video', null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_deportistas', null=True, blank=True)

#Composicion corporal
class ComposicionCorporal(models.Model):
    tipos_rh =(
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
    )
    deportista = models.ForeignKey(Deportista)
    peso = models.FloatField()
    estatura = models.FloatField()
    RH = models.CharField(max_length=4,choices=tipos_rh)
    talla_camisa = models.CharField(max_length=100)
    talla_pantaloneta = models.CharField(max_length=100)
    talla_zapato = models.CharField(max_length=100)
    porcentaje_grasa = models.CharField(max_length=100)
    porcentaje_musculo = models.CharField(max_length=100)


#Hitorial deportivo
class HistorialDeportivo(models.Model):
    tipo_his_deportivo=(
        ('Competencia','Competencia'),
        ('Premio','Premio'),
        ('Logro Deportivo','Logro Deportivo'),
        ('Participacion en Equipo','Participacion en Equipo'),
    )
    fecha = models.DateField()
    lugar = models.CharField(max_length=100)
    descripcion = models.TextField()
    institucion_equipo = models.CharField(max_length=100,blank=True,null=True)
    tipo = models.CharField(choices=tipo_his_deportivo,max_length=100,verbose_name='Tipo Historial')
    deportista = models.ForeignKey(Deportista)

#Informacion academica
class InformacionAcademica(models.Model):
    tipo_academica = (
        ('Jardin','Jardin'),
        ('Primaria','Primaria'),
        ('Bachillerato','Bachillerato'),
        ('Pregrado','Pregrado'),
        ('Postgrado','Postgrado'),
    )
    tipo_estado = (
        ('Finalizado','Finalizado'),
        ('Incompleto','Incompleto'),
        ('Actual','Actual'),
    )
    pais = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100) #si es diferente de colombia
    ciudad = models.CharField(max_length=100) #si es diferente de colombia
    institucion = models.CharField(max_length=100)
    nivel = models.CharField(choices=tipo_academica,max_length=20)
    grado_semestre = models.IntegerField()
    profesion =  models.CharField(max_length=100,blank=True,null=True)
    estado = models.CharField(choices=tipo_estado,max_length=20)
    fecha_finalizacion = models.DateField(blank=True,null=True)
    fecha_desercion = models.DateField(blank=True,null=True)
    deportista = models.ForeignKey(Deportista)