#encoding:utf-8

from entidades.models import *
from django.db import models


class Dirigente(models.Model):
    tipo_genero = (
        ('Hombre','Hombre'),
        ('Mujer','Mujer'),
    )
    tipo_identificacion = (
        ('CC', "Cédula de ciudadanía"),
        ('CE', "Cédula de extranjería"),
        ('PT', "Pasaporte"),
    )
    tipo_identificacion = models.CharField(choices=tipo_identificacion, max_length=2, verbose_name="Tipo de Identificación")
    identificacion = models.CharField(max_length=20, verbose_name="Número de Identificación")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    genero = models.CharField(choices=tipo_genero,max_length=6, verbose_name='Género')
    cargo = models.CharField(max_length=100)
    superior = models.ForeignKey('self', null=True, blank=True);
    telefono = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    descripcion = models.CharField(max_length=500, verbose_name="Descripción o Logros")
    fecha_posecion = models.DateField()
    fecha_retiro = models.DateField(null=True,blank=True)
    foto = models.ImageField(upload_to='fotos_dirigentes', null=True, blank=True)
    activo = models.BooleanField(default=True)

    entidad = models.ForeignKey(Entidad, null=True, blank=True)
    nacionalidad = models.ManyToManyField(Nacionalidad)

    def __str__(self):
        return '% %' % (self.nombres, self.apellidos)

class Funcion(models.Model):
    descripcion = models.CharField(max_length=200)
    dirigente = models.ForeignKey('Dirigente')


