#encoding:utf-8

from django.db import models
from entidades.models import Ciudad, Entidad

class CentroAcondicionamiento(models.Model):
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, verbose_name="dirección")
    telefono = models.CharField(max_length=50, verbose_name="teléfono")
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
    privado = models.PositiveIntegerField(default=0, verbose_name="Costo mensual al afiliado")
    publico = models.PositiveIntegerField(verbose_name="Costo mensual al público", default=0)
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