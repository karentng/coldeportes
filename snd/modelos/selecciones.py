#encoding:utf-8

from entidades.models import *
from django.db import models

class Seleccion(models.Model):
    TIPO_SELECCION = (
        (1,'Departamental'),
        (2,'Nacional'),
        (6,'Olimpica'),
        (8,'Departamental Paralimpica'), #Pendiente implementacion
        (7,'Nacional Paralimpica'), #Pendiente implementacion
        (10,'Paralimpica'), #Pendiente implementacion
    )
    TIPO_CAMPEONATO = (
        (1,'Amistoso'),
        (2,'Eliminatoria'),
        (3,'Profesional'),
    )
    ESTADOS_SELE = (
        (0,'Activo'),
    )
    fecha_inicial = models.DateField(verbose_name='Fecha de convocatoria')
    fecha_final = models.DateField(verbose_name='Fecha de finalización de convocatoria')
    nombre = models.CharField(max_length=100,verbose_name='Nombre de la Selección')
    campeonato = models.CharField(verbose_name='Nombre Campeonato',max_length=100)
    tipo = models.IntegerField(choices=TIPO_SELECCION,verbose_name='Tipo de Selección')
    tipo_campeonato = models.IntegerField(choices=TIPO_CAMPEONATO)
    estado = models.IntegerField(choices=ESTADOS_SELE,default=0)

    class Meta:
        permissions = (
            ("view_seleccion", "Permite ver seleccion"),
        )

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.campeonato = self.campeonato.upper()
        super(Seleccion, self).save(*args, **kwargs)

class DeportistasSeleccion(models.Model):
    deportista = models.CharField(max_length=100)
    entidad = models.ForeignKey(Entidad)
    seleccion = models.ForeignKey(Seleccion)

class PersonalSeleccion(models.Model):
    personal = models.CharField(max_length=100)
    entidad = models.ForeignKey(Entidad)
    seleccion = models.ForeignKey(Seleccion)
