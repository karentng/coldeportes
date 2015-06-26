#encoding:utf-8

from django.db import models
from entidades.models import Ciudad, Entidad

class CentroAcondicionamiento(models.Model):
    ESTADOS = (
        (1, "Activo"),
        (2, "Inactivo"),
    )
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, verbose_name="dirección")
    telefono = models.CharField(max_length=50, verbose_name="teléfono")
    email = models.EmailField()
    latitud = models.FloatField(max_length=10)
    longitud = models.FloatField(max_length=10)
    altura = models.FloatField(max_length=10)
    contacto = models.TextField(verbose_name='información de contacto', null=True, blank=True)
    entidad = models.ForeignKey(Entidad)    
    estado = models.IntegerField(choices=ESTADOS, default=1)
    ciudad = models.ForeignKey(Ciudad)

class CACostoUso(models.Model):
    centro = models.OneToOneField(CentroAcondicionamiento)
    privado = models.PositiveIntegerField(default=0, verbose_name="Costo mensual al afiliado")
    publico = models.PositiveIntegerField(verbose_name="Costo mensual al público", default=0)
    libre = models.BooleanField()

class CAServicios(models.Model):
    centro = models.OneToOneField(CentroAcondicionamiento)
    acondicionamiento = models.BooleanField(verbose_name="Acondicionamiento")
    fortalecimiento = models.BooleanField(verbose_name="Fortalecimiento")
    zona_cardio = models.BooleanField(verbose_name="Zona cardio")
    zona_humeda = models.BooleanField(verbose_name="Zona húmeda")
    medico = models.BooleanField(verbose_name="Médico")
    nutricionista = models.BooleanField(verbose_name="Nutricionista")
    fisioterapia = models.BooleanField(verbose_name="Fisioterapia")

    def __iter__(self):
        for field in self._meta.fields:
            vn = field.verbose_name
            valor = field.value_to_string(self)

            if vn == 'ID' or vn == 'centro' or valor == 'False':
                continue
            
            yield vn

class CAOtros(models.Model):
    centro = models.OneToOneField(CentroAcondicionamiento)
    camerinos = models.BooleanField(verbose_name="Camerinos")
    duchas = models.BooleanField(verbose_name="Duchas")
    comentarios = models.TextField(blank=True, null=True)

    def __iter__(self):
        for field in self._meta.fields:
            vn = field.verbose_name
            valor = field.value_to_string(self)

            if vn == 'ID' or vn == 'centro' or valor == 'False' or vn == 'comentarios':
                continue
            
            yield vn