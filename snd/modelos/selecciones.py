#encoding:utf-8

from entidades.models import *
from django.db import models
from .deportistas import Deportista
from .personal_apoyo import PersonalApoyo

class Seleccion(models.Model):
    TIPO_SELECCION = (
        (1,'Departamental'),
        (2,'Nacional'),
    )
    TIPO_CAMPEONATO = (
        (1,'Amistoso'),
        (2,'Eliminatoria'),
        (3,'Profesional'),
    )
    fecha_inicial = models.DateField(verbose_name='Fecha de convocatoria')
    fecha_final = models.DateField(verbose_name='Fecha de finalización de convocatoria')
    nombre = models.CharField(max_length=100,verbose_name='Nombre de la Selección')
    campeonato = models.CharField(verbose_name='Nombre Campeonato',max_length=100)
    tipo = models.IntegerField(choices=TIPO_SELECCION,verbose_name='Tipo de Selección')
    tipo_campeonato = models.IntegerField(choices=TIPO_CAMPEONATO)
    deportistas = models.ManyToManyField(Deportista,blank=True)
    personal_apoyo = models.ManyToManyField(PersonalApoyo,blank=True)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.campeonato = self.campeonato.upper()
        super(Seleccion, self).save(*args, **kwargs)

