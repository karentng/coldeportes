#encoding:utf-8

from entidades.models import *
from django.db import models
import os
from django.conf import settings


class Dirigente(models.Model):
    def foto_name(instance, filename):
        #el nombre de la imagen es la identificación del dirigente, filename[-4:] indica la extensión del archivo
        #primero se borra alguna imagen existente que tenga el mismo nombre. Si la imagen anterior tiene una extensión distinta a la nueva se crea una copia
        ruta = 'fotos_dirigentes/' + instance.identificacion + filename[-4:]
        ruta_delete = settings.MEDIA_ROOT + "/" + ruta
        if(os.path.exists(ruta_delete)):
            os.remove(ruta_delete)
        return ruta

    TIPO_GENERO = (
        ('Hombre','Hombre'),
        ('Mujer','Mujer'),
        ('LGTBI', 'LGTBI'),
    )
    TIPO_IDENTIFICACION = (
        ('CC', "Cédula de ciudadanía"),
        ('CE', "Cédula de extranjería"),
        ('PT', "Pasaporte"),
    )
    ESTADOS = (
        (1, "Activo"),
        (2, "Inactivo"),
    )

    tipo_identificacion = models.CharField(choices=TIPO_IDENTIFICACION, max_length=2, verbose_name="Tipo de identificación")
    identificacion = models.CharField(max_length=20, verbose_name="Número de identificación", unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    genero = models.CharField(choices=TIPO_GENERO,max_length=6, verbose_name='Género')
    cargo = models.CharField(max_length=100, verbose_name="Nombre del cargo")
    superior = models.ForeignKey('self', null=True, blank=True);
    telefono = models.CharField(max_length=100, verbose_name="Teléfono")
    email = models.EmailField(null=True,blank=True)
    nacionalidad = models.ManyToManyField(Nacionalidad)
    fecha_posesion = models.DateField(verbose_name="Fecha de posesión")
    fecha_retiro = models.DateField(null=True,blank=True, verbose_name="Fecha de retiro")
    estado = models.IntegerField(choices=ESTADOS, default=1, verbose_name="Estado del dirigente")
    foto = models.ImageField(upload_to=foto_name, null=True, blank=True)
    descripcion = models.CharField(max_length=500, verbose_name="Descripción o logros")

    entidad = models.ForeignKey(Entidad, null=True, blank=True)
    

    def __str__(self):
        return "{0} {1} - {2}".format(self.nombres, self.apellidos, self.cargo)

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Dirigente, self).save(*args, **kwargs)

class Funcion(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    dirigente = models.ForeignKey(Dirigente)


