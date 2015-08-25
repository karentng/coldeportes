#encoding:utf-8

from entidades.models import *
from django.db import models

class Escenario(models.Model):
    estratos = (
        ('1', 'Uno'),
        ('2', 'Dos'),
        ('3', 'Tres'),
        ('4', 'Cuatro'),
        ('5', 'Cinco'),
        ('6', 'Seis'),
    )
    ESTADOS = (
        (0,'ACTIVO'),
        (1,'INACTIVO'),
        (2,'EN TRANSFERENCIA'),
        (3,'TRANSFERIDO'),
    )
    nombre =  models.CharField(max_length=100,unique=True)
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
    estado = models.IntegerField(choices=ESTADOS, default=0, verbose_name="estado del Escenario")
    descripcion = models.CharField(max_length=1024, verbose_name='descripción', null=True)

class CaracterizacionEscenario(models.Model):   
    accesos = (
        ('pr', 'Privado'),
        ('dul', 'De Uso Libre'),
        ('pcp', 'Público Con Pago'),
    )
    escenario = models.ForeignKey(Escenario)
    capacidad_espectadores = models.CharField(max_length=50, verbose_name='capacidad de zona espectadores')
    metros_construidos = models.CharField(max_length=50, verbose_name='metros cuadrados construídos')
    tipo_escenario = models.ForeignKey(TipoEscenario)
    tipo_disciplinas = models.ManyToManyField(TipoDisciplinaDeportiva)
    tipo_superficie_juego = models.ManyToManyField(TipoSuperficie)
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
    titulo = models.CharField(max_length=255, verbose_name="título")
    foto = models.ImageField(upload_to='fotos_escenarios', null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True, max_length=1024)


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
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    descripcion = models.CharField(max_length=1024, null=True)
